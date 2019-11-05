-- Create the database structure
CREATE TABLE IF NOT EXISTS "emails" (
  "email" VARCHAR(50) NOT NULL UNIQUE,
  "hash" VARCHAR(128) NOT NULL UNIQUE,
  PRIMARY KEY("email")
);

CREATE TABLE IF NOT EXISTS "writers" (
  "uid" VARCHAR(30) NOT NULL UNIQUE,
  "handle" VARCHAR(20) NOT NULL,
  PRIMARY KEY("uid")
);

CREATE TABLE IF NOT EXISTS "writer_dates" (
  "uid" VARCHAR(30) NOT NULL,
  "date" VARCHAR(7) NOT NULL,
  PRIMARY KEY("uid","date"),
  FOREIGN KEY ("uid") REFERENCES writers("uid")
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "tweets" (
  "tweet_id" VARCHAR(25) NOT NULL UNIQUE,
  "date" DATE NOT NULL,
  "uid" VARCHAR(30) NOT NULL,
  "content" VARCHAR(512) NOT NULL,
  "word" VARCHAR(25) NOT NULL,
  "media" VARCHAR(512),
  PRIMARY KEY("tweet_id"),
  FOREIGN KEY ("uid") REFERENCES writers("uid")
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);
