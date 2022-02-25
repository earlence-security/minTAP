DROP TABLE IF EXISTS top_post;

CREATE TABLE top_post (
  id VARCHAR(6) PRIMARY KEY,
  subreddit TEXT NOT NULL,
  title TEXT,
  content TEXT,
  post_url TEXT,
  timestamp INTEGER
);

DROP TABLE IF EXISTS test_data;

CREATE TABLE test_data (
  id VARCHAR(6) PRIMARY KEY,
  subreddit TEXT NOT NULL,
  title TEXT,
  content TEXT,
  post_url TEXT,
  timestamp INTEGER
);






