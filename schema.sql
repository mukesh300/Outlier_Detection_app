DROP TABLE IF EXISTS user_data;

CREATE TABLE user_data (
    username text PRIMARY KEY,
    password text
);

INSERT INTO user_data
VALUES
    ("root", "root");

DROP TABLE IF EXISTS product;

CREATE TABLE product (
    time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status text
);