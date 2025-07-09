-- Migration script to create fees table

CREATE TABLE IF NOT EXISTS fees (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    date TIMESTAMP NOT NULL,
    amount FLOAT NOT NULL,
    reason VARCHAR(255) NOT NULL
);
