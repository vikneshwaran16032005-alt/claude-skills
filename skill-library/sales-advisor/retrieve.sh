#!/usr/bin/env bash
# Live corpus pull for the sales-advisor. Queries the chroma operator_brain index,
# filtered to the sales-relevant niches, and returns real transcript chunks with the
# operator who said them. This is the "live" half of the hybrid brain.
#
# Usage:
#   ./retrieve.sh "how to handle the price objection" [k]
#   ./retrieve.sh "cold call opener that books the meeting" 8
#
# Niches it draws from: Sales, Negotiation, Client Acquisition.
# Output: JSON (chunk text + creator + niche + url) so the skill can cite sources.

Q="${1:?usage: retrieve.sh \"query\" [k]}"
K="${2:-6}"
PY="/Users/vik/OperatorBrain/retrieval/.venv/bin/python"
R="/Users/vik/OperatorBrain/retrieval/retrieve.py"

# Pull from each sales niche, merge. retrieve.py supports one --niche per call,
# so we run the three and concatenate JSON results.
for N in "Sales" "Negotiation" "Client Acquisition"; do
  "$PY" "$R" "$Q" --k "$K" --niche "$N" --json 2>/dev/null
done
