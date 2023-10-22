CREATE TABLE domains (
    id INTEGER PRIMARY KEY,
    domain VARCHAR NOT NULL,
    http_code INTEGER,
    title VARCHAR(255),
    description VARCHAR(255),
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (domain)
);
