-- Create the database structure
CREATE TABLE IF NOT EXISTS "emails" (
  "email" VARCHAR(50) NOT NULL UNIQUE,
  PRIMARY KEY("email")
);

CREATE TABLE IF NOT EXISTS "givers" (
  "uid" VARCHAR(30) NOT NULL UNIQUE,
  "handle" VARCHAR(20) NOT NULL,
  "date" VARCHAR(7) NOT NULL UNIQUE,
  PRIMARY KEY("uid")
);

CREATE TABLE IF NOT EXISTS "tweets" (
  "tweet_id" VARCHAR(25) NOT NULL UNIQUE,
  "date" DATE NOT NULL UNIQUE,
  "uid" VARCHAR(30) NOT NULL,
  "content" VARCHAR(512) NOT NULL,
  "word" VARCHAR(25) NOT NULL,
  "media" VARCHAR(512),
  PRIMARY KEY("tweet_id"),
  FOREIGN KEY ("uid") REFERENCES givers("uid")
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);
