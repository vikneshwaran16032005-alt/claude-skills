#!/usr/bin/env python3
"""One-time LinkedIn login. Opens a browser; YOU log in manually; saves the session.
No password is handled by the agent."""
import asyncio, os
from pathlib import Path
from linkedin_scraper import BrowserManager, wait_for_manual_login

SESSION = os.environ.get("LINKEDIN_SESSION",
                         str(Path.home() / ".config" / "linkedin-scraper" / "session.json"))

async def main():
    Path(SESSION).parent.mkdir(parents=True, exist_ok=True)
    async with BrowserManager(headless=False) as browser:
        await browser.page.goto("https://www.linkedin.com/login")
        print("\n>>> Log in to LinkedIn in the opened browser window (you have 5 minutes).")
        print(">>> Resolve any 2FA / checkpoint there too.\n")
        await wait_for_manual_login(browser.page, timeout=300)
        await browser.save_session(SESSION)
        try:
            os.chmod(SESSION, 0o600)
        except OSError:
            pass
        print("\n[OK] Session saved to", SESSION)

if __name__ == "__main__":
    asyncio.run(main())
