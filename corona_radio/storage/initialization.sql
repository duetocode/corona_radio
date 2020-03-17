CREATE TABLE subscription (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(128) NOT NULL,
    description VARCHAR(1024) NULL,
    link VARCHAR(2048) NULL,
    image VARCHAR(2048) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE podcast (
    id VARCHAR(512) NOT NULL,
    subscription_id INTEGER NOT NULL,
    title VARCHAR(128) NOT NULL,
    description VARCHAR(1024) NULL,
    publish_date LONG NOT NULL DEFAULT current_timestamp,
    url VARCHAR(2048) NULL,
    length INT NULL,
    downloaded INT NOT NULL DEFAULT 0,
    PRIMARY KEY (subscription_id, id)
);

CREATE TABLE download_queue (
    podcast_id VARCHAR(512) NOT NULL,
    subscription_id INTEGER NOT NULL,
    priority INTEGER NOT NULL DEFAULT 0,
    published_date LONG NOT NULL,
    PRIMARY KEY (subscription_id, podcast_id)
);