#!/usr/bin/env python3
"""Scrape a LinkedIn profile / company / company posts / job search using a saved session.
Outputs JSON to stdout. Requires a session created by login.py."""
import asyncio, argparse, json, os, sys
from pathlib import Path

SESSION = os.environ.get("LINKEDIN_SESSION",
                         str(Path.home() / ".config" / "linkedin-scraper" / "session.json"))

def to_jsonable(obj):
    if hasattr(obj, "model_dump"):          # pydantic v2
        return obj.model_dump()
    if hasattr(obj, "dict"):                # pydantic v1 fallback
        return obj.dict()
    if isinstance(obj, list):
        return [to_jsonable(x) for x in obj]
    return obj

async def run(a):
    if not Path(SESSION).exists():
        print(json.dumps({"error": "No session found. Run login.py first to authenticate.",
                          "session_path": SESSION}))
        sys.exit(2)
    from linkedin_scraper import (BrowserManager, PersonScraper, CompanyScraper,
                                  JobSearchScraper, CompanyPostsScraper)
    async with BrowserManager(headless=True) as browser:
        await browser.load_session(SESSION)
        page = await browser.new_page()
        if a.type == "person":
            result = await PersonScraper(page).scrape(a.url)
        elif a.type == "company":
            result = await CompanyScraper(page).scrape(a.url)
        elif a.type == "posts":
            result = await CompanyPostsScraper(page).scrape(a.url, limit=a.limit)
        elif a.type == "jobs":
            result = await JobSearchScraper(page).search(
                keywords=a.keywords, location=a.location, limit=a.limit)
        else:
            print(json.dumps({"error": f"unknown type {a.type}"})); sys.exit(1)
    print(json.dumps(to_jsonable(result), indent=2, default=str))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--type", required=True, choices=["person", "company", "posts", "jobs"])
    p.add_argument("--url", default=None)
    p.add_argument("--keywords", default=None)
    p.add_argument("--location", default=None)
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args()
    if args.type in ("person", "company", "posts") and not args.url:
        print(json.dumps({"error": "--url is required for this type"})); sys.exit(1)
    if args.type == "jobs" and not args.keywords:
        print(json.dumps({"error": "--keywords is required for jobs"})); sys.exit(1)
    asyncio.run(run(args))
