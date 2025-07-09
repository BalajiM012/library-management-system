-- Migration script to create borrow_records table

CREATE TABLE IF NOT EXISTS borrow_records (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    book_id INTEGER NOT NULL REFERENCES book(id),
    borrow_date TIMESTAMP NOT NULL,
    due_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP,
    fine FLOAT DEFAULT 0.0
);
