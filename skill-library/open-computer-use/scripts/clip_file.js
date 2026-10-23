ObjC.import('AppKit');
function run(argv) { const pb = $.NSPasteboard.generalPasteboard; pb.clearContents; return pb.writeObjects($.NSArray.arrayWithObject($.NSURL.fileURLWithPath(argv[0]))) ? 'file on clipboard' : 'failed'; }
