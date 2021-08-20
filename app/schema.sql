DROP TABLE IF EXISTS daily_records;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS songs;

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  authorization_code VARCHAR(255) NOT NULL,
  refresh_token VARCHAR(255) NOT NULL
);

CREATE TABLE songs (
  uri VARCHAR(255) PRIMARY KEY,
  user_id INTEGER NOT NULL,
  listen_time TIMESTAMP NOT NULL,
  mood TEXT NOT NULL,
  song_uri TEXT NOT NULL,
  danceability NUMERIC NOT NULL,
  key INTEGER NOT NULL,
  loudness NUMERIC NOT NULL,
  mode INTEGER NOT NULL,
  speechiness NUMERIC NOT NULL,
  acousticness NUMERIC NOT NULL,
  instrumentalness NUMERIC NOT NULL,
  liveness NUMERIC NOT NULL,
  valence NUMERIC NOT NULL,
  tempo NUMERIC NOT NULL,
  duration_ms INTEGER NOT NULL,
  time_signature INTEGER NOT NULL
);

CREATE TABLE daily_records (
  date TIMESTAMP NOT NULL,
  mood VARCHAR(255) NOT NULL,
  song_uri VARCHAR(255) NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id),
  CONSTRAINT daily_record_of_user PRIMARY KEY(user_id, date)
); 
