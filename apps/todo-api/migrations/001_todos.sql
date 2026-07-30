-- F1 SPEC todos table
CREATE TABLE IF NOT EXISTS todos (
  id TEXT PRIMARY KEY NOT NULL,
  title TEXT NOT NULL,
  completed INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
