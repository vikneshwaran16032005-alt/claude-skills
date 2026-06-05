#!/usr/bin/env bash
# scaffold.sh — copy templates and apply placeholder substitutions.
#
# Usage:
#   scaffold.sh \
#     --out <output_dir> \
#     --client-name "<Brand Name>" \
#     --client-domain "<example.com>" \
#     --client-slug "<kebab-slug>" \
#     --email-from "noreply@example.com" \
#     --composio-user-id "you@example.com" \
#     --business-email "billing@example.com" \
#     --mongodb-db "<dbname>"
#
# Copies templates/frontend/ → <out>/<slug>/ and templates/backend/ → <out>/<slug>_backend/,
# then replaces {{PLACEHOLDER}} tokens in all text files.

set -euo pipefail

# --- parse args ----------------------------------------------------------
OUT_DIR=""
CLIENT_NAME=""
CLIENT_DOMAIN=""
CLIENT_SLUG=""
EMAIL_FROM=""
COMPOSIO_USER_ID=""
BUSINESS_EMAIL=""
MONGODB_DB=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT_DIR="$2"; shift 2 ;;
    --client-name) CLIENT_NAME="$2"; shift 2 ;;
    --client-domain) CLIENT_DOMAIN="$2"; shift 2 ;;
    --client-slug) CLIENT_SLUG="$2"; shift 2 ;;
    --email-from) EMAIL_FROM="$2"; shift 2 ;;
    --composio-user-id) COMPOSIO_USER_ID="$2"; shift 2 ;;
    --business-email) BUSINESS_EMAIL="$2"; shift 2 ;;
    --mongodb-db) MONGODB_DB="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

for var in OUT_DIR CLIENT_NAME CLIENT_DOMAIN CLIENT_SLUG EMAIL_FROM COMPOSIO_USER_ID BUSINESS_EMAIL MONGODB_DB; do
  if [[ -z "${!var}" ]]; then
    echo "Missing required flag for $var" >&2
    exit 1
  fi
done

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_SRC="$SKILL_DIR/templates/frontend"
BACKEND_SRC="$SKILL_DIR/templates/backend"
FRONTEND_DEST="$OUT_DIR/$CLIENT_SLUG"
BACKEND_DEST="$OUT_DIR/${CLIENT_SLUG}_backend"

if [[ -e "$FRONTEND_DEST" || -e "$BACKEND_DEST" ]]; then
  echo "Refusing to overwrite existing $FRONTEND_DEST or $BACKEND_DEST" >&2
  exit 1
fi

mkdir -p "$OUT_DIR"
cp -R "$FRONTEND_SRC" "$FRONTEND_DEST"
cp -R "$BACKEND_SRC" "$BACKEND_DEST"

# --- substitute placeholders --------------------------------------------
substitute() {
  local dest="$1"
  # Skip binaries (favicon, svgs) and node_modules (none yet, but defensive).
  find "$dest" -type f \
    ! -name '*.ico' \
    ! -name '*.png' \
    ! -name '*.jpg' \
    ! -name '*.jpeg' \
    ! -name '*.gif' \
    ! -name '*.webp' \
    ! -path '*/node_modules/*' \
    -print0 \
  | while IFS= read -r -d '' f; do
      LC_ALL=C sed -i '' \
        -e "s|{{CLIENT_NAME}}|$CLIENT_NAME|g" \
        -e "s|{{CLIENT_DOMAIN}}|$CLIENT_DOMAIN|g" \
        -e "s|{{CLIENT_SLUG}}|$CLIENT_SLUG|g" \
        -e "s|{{EMAIL_FROM}}|$EMAIL_FROM|g" \
        -e "s|{{COMPOSIO_USER_ID}}|$COMPOSIO_USER_ID|g" \
        -e "s|{{BUSINESS_EMAIL}}|$BUSINESS_EMAIL|g" \
        -e "s|{{MONGODB_DB}}|$MONGODB_DB|g" \
        "$f"
    done
}

substitute "$FRONTEND_DEST"
substitute "$BACKEND_DEST"

# --- sanity check: any unsubstituted placeholders left? ------------------
LEFTOVER="$(grep -rEl '\{\{[A-Z_]+\}\}' "$FRONTEND_DEST" "$BACKEND_DEST" 2>/dev/null || true)"
if [[ -n "$LEFTOVER" ]]; then
  echo "WARNING: unsubstituted placeholders remain in:" >&2
  echo "$LEFTOVER" >&2
fi

echo "Frontend → $FRONTEND_DEST"
echo "Backend  → $BACKEND_DEST"
