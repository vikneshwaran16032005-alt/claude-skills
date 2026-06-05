import { MongoClient } from "mongodb";

declare global {
  var _mongoClientPromise: Promise<MongoClient> | undefined;
}

async function connect(): Promise<MongoClient> {
  const uri = process.env.MONGODB_URI;
  if (!uri) {
    throw new Error(
      "MONGODB_URI is not set. Add it to .env.local before signing in or hitting the database.",
    );
  }
  return new MongoClient(uri).connect();
}

function buildClientPromise(): Promise<MongoClient> {
  if (process.env.NODE_ENV === "development") {
    if (!global._mongoClientPromise) global._mongoClientPromise = connect();
    return global._mongoClientPromise;
  }
  return connect();
}

// Lazy: the error only surfaces when something actually awaits the client,
// so the app boots even if MONGODB_URI is missing (you just can't sign in).
export const clientPromise: Promise<MongoClient> = buildClientPromise();
// Attach a no-op catch so a missing URI doesn't surface as an unhandledRejection
// before a real consumer (Auth.js adapter, getDb()) awaits it.
clientPromise.catch(() => {});

export async function getDb() {
  const client = await clientPromise;
  return client.db(process.env.MONGODB_DB ?? "{{MONGODB_DB}}");
}
