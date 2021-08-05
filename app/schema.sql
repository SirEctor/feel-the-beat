
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS songs;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE songs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  listen_time TIMESTAMP NOT NULL,
  mood TEXT NOT NULL,
  song_uri TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);