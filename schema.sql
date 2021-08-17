DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS daily_records;


CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  authorization_code VARCHAR(255) NOT NULL,
  refresh_token VARCHAR(255) NOT NULL
);

CREATE TABLE songs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  listen_time TIMESTAMP NOT NULL,
  mood TEXT NOT NULL,
  song_uri TEXT NOT NULL,
  id VARCHAR(255) PRIMARY KEY,
  danceability NUMERIC(1, 4) NOT NULL,
  key INTEGER NOT NULL,
  loudness NUMERIC(2, 4) NOT NULL,
  mode INTEGER NOT NULL,
  speechiness NUMERIC(1, 4) NOT NULL,
  acousticness NUMERIC(1, 4) NOT NULL,
  instrumentalness NUMERIC(1, 4) NOT NULL,
  liveness NUMERIC(1, 4) NOT NULL,
  valence NUMERIC(1, 4) NOT NULL,
  tempo NUMERIC(2, 4) NOT NULL
  uri VARCHAR(255) NOT NULL,
  duration_ms INTEGER NOT NULL,
  time_signature INTERGER NOT NULL
);

CREATE TABLE daily_records (
  date TIMESTAMP NOT NULL,
  mood VARCHAR(255) NOT NULL,
  song_uri VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
  CONSTRAINT daily_record_of_user PRIMARY KEY(user_id, date)
);