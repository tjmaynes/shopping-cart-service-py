-- migrate:up
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    name VARCHAR (255) NOT NULL,
    price BIGINT NOT NULL,
    manufacturer VARCHAR (255) NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    last_modified_at  TIMESTAMP DEFAULT current_timestamp
);

-- migrate:down
DROP TABLE IF EXISTS cart;