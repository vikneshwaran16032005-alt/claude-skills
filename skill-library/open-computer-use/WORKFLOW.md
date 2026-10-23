# Background computer use: Vik's workflow (v2, 2026-10-15)

Goal: operate desktop apps without moving Vik's cursor, typing on his keyboard, raising windows or changing his front app. Tested on this Mac with Calculator, TextEdit, Finder and Buzz.

## 0. One-time setup (done, keep it this way)

| Piece | Where | Why |
|---|---|---|
| open-computer-use CLI and MCP | `~/.local/bin/open-computer-use`, `~/.local/bin/ocu` (wrappers) | Accessibility plus SkyLight background input |
| Agent cursor overlay off | `OPEN_COMPUTER_USE_VISUAL_CURSOR=0` in both wrappers and the MCP `env` in `~/.claude.json` | The overlay looked like a second mouse |
| Stop hook | `~/.claude/settings.json`: `open-computer-use turn-ended` | Restores parked windows and hides overlays when a turn ends |
| Runner | `~/.local/bin/ocu-bg` | Runs a task script and prints only its result line |
| Helpers | `scripts/bg-prelude.js` (next to this file) | `park`, `tap`, `typeIn`, `key`, `grep`, `find`, `unpark`, `result` |
| macOS permissions | Accessibility and Screen Recording for open-computer-use | Already granted by Vik |

Check health with `open-computer-use doctor` when something fails.

## 1. Pick the cheapest route first

1. An API, CLI, file edit or connector (Gmail, Drive, Calendar, Apify).
2. A website: the built-in browser tools or Playwright, not desktop clicks.
3. A desktop app with no other route: this workflow.

## 2. Look before acting (one filtered read)

```sh
ocu-bg - <<'JS'
result(await grep("Buzz", /button|text field|text area/));
JS
```

- `grep` re-reads the app and returns only matching lines, about 0.1 to 1k tokens instead of 2 to 9k with a screenshot.
- Each line is `<index> <role> <label> [Help: ...] [ID: ...]`. Prefer the stable `ID:` (for example `ID: Seven`), then the exact role and label.
- Use `await shot(app)` only when layout or colour matters (about 1.5k tokens).
- If the app is not running, start it with `open -g -a "<App>"` (`-g` keeps it in the background).

## 3. Write the task as one script

Example shape (labels and IDs here are placeholders; take the real ones from step 2):

```sh
ocu-bg - <<'JS'
const A = "Buzz";
await park(A);                                    // move its window to the invisible agent display
const log = [];
log.push(await tap(A, { role: "text field", label: "Name" }));   // focus by exact label
await typeIn(A, "Call Prep");                     // sky_key typing, no real keyboard
log.push(await tap(A, { id: "SaveButton" }));     // ask Vik first if this sends, saves externally, deletes or buys
const check = await grep(A, /Call Prep/);         // read back to verify
await unpark(A);                                  // return the window exactly where it was
result({ log, check });
JS
```

Rules inside the script:
- Every `tap` and `find` re-reads the app first, so element numbers are never reused after the UI changes. Never hard-code an index.
- A missing target returns `{ skipped }` and nothing is clicked. Read again and adjust; never guess.
- Web and Electron fields (Buzz, Slack, Chrome): `tap` the field or its label, then `typeIn`. `setValue` does not reach React forms.
- Native fields (TextEdit, Notes, Calculator): `setValue` via `(await bind(A)).setValue(idx, text)` is fine and fast for long text.
- Keys: only `key(A, "tab")` or `key(A, "return")`, which use `sky_key`. Never plain `press_key`, Escape or cmd+w on a window.
- Coordinate clicks only when no element exists: `(await bind(A)).click([x, y], { clickMethod: "sky_click" })`.

## 4. Verify, then report

Do not claim success without a read-back (`grep`, `find`, or a final `shot` if visual). Report what changed and what was skipped.

## 5. Stop for Vik before irreversible steps

Stop the script before the final send, submit, publish, delete, purchase or permission grant. Show Vik what will happen, wait for a yes, then run only that last step in a new script.

## 6. Clean up

- `unpark(A)` at the end (the Stop hook and the runtime exit also restore, but do it explicitly).
- Quit throwaway apps with `pkill -x "<App>"`, never through the UI.
- Never trigger save or close dialogs. If one appears, leave it and tell Vik.

## Hard rules (learned 2026-10-13)

1. Never click a remembered element number; resolve by ID or exact label from a fresh read, or skip.
2. Never use plain `press_key`, Escape or cmd+w on a window. Plain key presses pulled TextEdit to the front and took Vik's typing.
3. Never trigger save/close dialogs; quit test apps with `pkill`.
4. Never move the real pointer: no `click_method: "global"`, and never set `OPEN_COMPUTER_USE_ALLOW_GLOBAL_POINTER_FALLBACKS`.
5. Keep the overlay off (`OPEN_COMPUTER_USE_VISUAL_CURSOR=0`).
6. Ask before sending, deleting, buying, publishing or approving anything.
7. Do not open password managers or unrelated private apps.

## Limits

| Limit | Workaround |
|---|---|
| Drag (select text, move windows, Finder drag-and-drop) has no effect in background mode | Keyboard selection, `setValue`, shell `mv`/`cp`, the app's own buttons |
| Hidden apps (cmd+h) refuse `sky_key` | Unhide with `open -g -a "<App>"`, then `park` |
| Windows on another Space or covered | `park` first (the agent display renders them) |
| Some Chromium buttons ignore accessibility clicks | `click([x, y], { clickMethod: "sky_click" })` |
| macOS updates can break SkyLight paths | Run the Calculator self-test below after an upgrade |

## Cost reference (measured)

| Method | Tokens per step |
|---|---|
| Old: `call --calls` with full state and screenshot | Calculator about 1.7k, TextEdit 2.8k (8.8k with full text), Buzz 3.2k; 12+34 took about 33.5k |
| New: `ocu-bg` with filtered result | About 50 to 300 tokens per task result; 12+34 took about 150 characters and 4 s |

## Self-test (about 4 s, background only)

```sh
open -g -a Calculator && sleep 1.5 && ocu-bg - <<'JS'
const A = "Calculator"; await park(A);
for (const id of ["AllClear","One","Two","Add","Three","Four","Equals"]) await tap(A, { id });
result({ display: await grep(A, /Edit field/) }); await unpark(A);
JS
pkill -x Calculator
```

Expected: `Edit field 46`.

## Recipe: send a file in a chat app (WhatsApp, tested 2026-10-15)

File pickers are dialogs, so attach by paste instead:
1. `osascript -l JavaScript scripts/clip_save.js <tmpdir>` (saves Vik's clipboard, all types).
2. `osascript -l JavaScript scripts/clip_file.js "<file>"` (puts the file on the clipboard).
3. `ocu-bg`: `park`, check the chat header (WhatsApp: `ID: NavigationBar_HeaderViewButton`), `tap` the composer (`ChatBar_ComposerTextView`), `key(A, "cmd+v")`, wait 2 s, `grep` the preview (file name, recipient chip `WAMultiSendBottomBarView_AudienceSelector_ContactChip`), `unpark`.
4. `osascript -l JavaScript scripts/clip_restore.js <tmpdir>` right away, then delete `<tmpdir>`.
5. Only after Vik asked for this send: re-check file and recipient, `tap` `WAMultiSendBottomBarView_SendButton`, then verify a "Your document, <name> ... Sent to <name>" line.
