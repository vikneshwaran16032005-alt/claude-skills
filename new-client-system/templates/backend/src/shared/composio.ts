import { realpathSync } from "node:fs";
import { tmpdir } from "node:os";
import { Composio } from "@composio/core";

const REAL_TMPDIR = (() => {
  try {
    return realpathSync(tmpdir());
  } catch {
    return tmpdir();
  }
})();

let _client: Composio | null = null;

export function composio(): Composio {
  if (!_client) {
    if (!process.env.COMPOSIO_API_KEY) {
      throw new Error("Missing COMPOSIO_API_KEY");
    }
    _client = new Composio({
      apiKey: process.env.COMPOSIO_API_KEY,
      // Tasks render PDFs to /tmp and pass absolute paths to Composio. We allow
      // auto-upload from /tmp + its realpath (on macOS, /tmp is a symlink to
      // /private/tmp; both must be allowlisted).
      dangerouslyAllowAutoUploadDownloadFiles: true,
      fileUploadDirs: [REAL_TMPDIR, "/tmp", "/private/tmp"],
    } as never);
  }
  return _client;
}

export function composioUserId(): string {
  const id = process.env.COMPOSIO_USER_ID;
  if (!id) throw new Error("Missing COMPOSIO_USER_ID");
  return id;
}

// Composio 0.10 requires an explicit toolkit version for manual execution.
// "latest" + dangerouslySkipVersionCheck keeps us on the newest schema.
const EXECUTE_OPTS = {
  version: "latest" as const,
  dangerouslySkipVersionCheck: true,
};

export async function sendGmailWithAttachment(args: {
  recipientEmail: string;
  subject: string;
  body: string;
  attachmentPath?: string;
}): Promise<unknown> {
  return composio().tools.execute(
    "GMAIL_SEND_EMAIL",
    {
      userId: composioUserId(),
      arguments: {
        recipient_email: args.recipientEmail,
        subject: args.subject,
        body: args.body,
        is_html: false,
        ...(args.attachmentPath ? { attachment: args.attachmentPath } : {}),
      },
      ...EXECUTE_OPTS,
    } as never,
  );
}

export async function uploadPdfToDrive(args: {
  filePath: string;
  fileName: string;
  folderId?: string;
}): Promise<unknown> {
  return composio().tools.execute(
    "GOOGLEDRIVE_UPLOAD_FILE",
    {
      userId: composioUserId(),
      arguments: {
        file_name: args.fileName,
        mime_type: "application/pdf",
        file_to_upload: args.filePath,
        ...(args.folderId ? { folder_id: args.folderId } : {}),
      },
      ...EXECUTE_OPTS,
    } as never,
  );
}
