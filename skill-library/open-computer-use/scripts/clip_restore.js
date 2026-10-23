ObjC.import('AppKit'); ObjC.import('Foundation');
function run(argv) {
  const dir = argv[0], pb = $.NSPasteboard.generalPasteboard;
  const index = JSON.parse(ObjC.unwrap($.NSString.stringWithContentsOfFileEncodingError(dir + '/index.json', $.NSUTF8StringEncoding, null)));
  const arr = $.NSMutableArray.array;
  for (const entry of index) { const it = $.NSPasteboardItem.alloc.init; for (const [t, f] of entry) it.setDataForType($.NSData.dataWithContentsOfFile(f), t); arr.addObject(it); }
  pb.clearContents; if (index.length) pb.writeObjects(arr);
  return 'restored ' + index.length + ' item(s)';
}
