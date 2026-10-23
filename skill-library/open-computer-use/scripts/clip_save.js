ObjC.import('AppKit'); ObjC.import('Foundation');
function run(argv) {
  const dir = argv[0], pb = $.NSPasteboard.generalPasteboard, items = pb.pasteboardItems, index = [];
  for (let i = 0; i < items.count; i++) {
    const it = items.objectAtIndex(i), types = it.types, entry = [];
    for (let j = 0; j < types.count; j++) {
      const t = ObjC.unwrap(types.objectAtIndex(j)), d = it.dataForType(t);
      if (d.isNil()) continue;
      const f = dir + '/' + i + '_' + j + '.bin'; d.writeToFileAtomically(f, true); entry.push([t, f]);
    }
    index.push(entry);
  }
  $(JSON.stringify(index)).writeToFileAtomicallyEncodingError(dir + '/index.json', true, $.NSUTF8StringEncoding, null);
  return 'saved ' + index.length + ' item(s), changeCount ' + pb.changeCount;
}
