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
  author TEXT NOT NULL,
  title TEXT,
  content TEXT,
  post_url TEXT,
  timestamp INTEGER
);


INSERT OR IGNORE INTO test_data(id,author,title,content,post_url,timestamp)
                 VALUES(1, 'Alice', 'Title 1', 'Body 1', 'https://example.com', 1646168693);
INSERT OR IGNORE INTO test_data(id,author,title,content,post_url,timestamp)
                 VALUES(2, 'Alice', 'Title 2', 'Body 2', 'https://example.com', 1646168714);
INSERT OR IGNORE INTO test_data(id,author,title,content,post_url,timestamp)
                 VALUES(3, 'Alice', 'Title 3', 'Body 3', 'https://example.com', 1646168719);




