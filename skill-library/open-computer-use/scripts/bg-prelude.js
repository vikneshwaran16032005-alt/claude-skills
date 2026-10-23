// Background computer-use helpers for `ocu js` (open-computer-use).
// Prepended to every task by ocu-bg. Every lookup re-reads the app,
// so element numbers are never reused after the UI changes.
var __apps = {};
async function bind(name) { return __apps[name] ??= await cua.getApp(name); }
function parseTree(text) {
  return text.split("\n").map(l => {
    const m = l.match(/^\s*(\d+)\s+(.*)$/);
    if (!m) return null;
    const rest = m[2];
    const id = (rest.match(/ ID: (.+?)(?:, Secondary Actions:|$)/) || [])[1];
    const desc = (rest.match(/ Description: (.+?)(?: ID:| Help:|, Secondary Actions:|$)/) || [])[1];
    return { idx: m[1], rest, id: id && id.trim(), desc: desc && desc.trim(), line: l.trim() };
  }).filter(Boolean);
}
function labelOf(el, role) {
  if (!el.rest.startsWith(role + " ")) return null;
  return el.rest.slice(role.length + 1).split(/ Help: | ID: | Description: | Value: |, Secondary Actions: /)[0].trim();
}
// spec: { id } or { role, label } or { role, desc }. Exact matches only, never fuzzy.
function match(el, spec) {
  if (spec.id !== undefined) return el.id === spec.id;
  if (spec.desc !== undefined) return el.rest.startsWith(spec.role + " ") && el.desc === spec.desc;
  return labelOf(el, spec.role) === spec.label;
}
async function state(app) { return (await bind(app)).getAXState({ emit: false }); }
async function find(app, spec) { const el = parseTree(await state(app)).find(e => match(e, spec)); return el ? el.idx : null; }
async function tap(app, spec, opts = {}) {
  const idx = await find(app, spec);
  if (idx === null) return { skipped: spec };
  await (await bind(app)).click(idx, opts);
  return { ok: spec };
}
async function typeIn(app, text) { await (await bind(app)).typeText(text, { keyMethod: "sky_key" }); }
async function key(app, k) { await (await bind(app)).pressKey(k, { keyMethod: "sky_key" }); }
async function park(app) { await (await bind(app)).getAXState({ emit: false, windowPlacement: "agent_display" }); }
async function unpark(app) { await (await bind(app)).getAXState({ emit: false, windowPlacement: "restore" }); }
async function grep(app, re) { return parseTree(await state(app)).filter(e => re.test(e.line)).map(e => e.line); }
// Saves a PNG for Claude to open with its Read tool. Use only when layout or colour matters.
async function shot(app, path = "/tmp/ocu-shot.png") {
  const bytes = await (await bind(app)).getScreenshot({ emit: false });
  (await import("node:fs")).writeFileSync(path, bytes);
  return path;
}
function result(obj) { nodeRepl.write("@@R " + JSON.stringify(obj)); }
