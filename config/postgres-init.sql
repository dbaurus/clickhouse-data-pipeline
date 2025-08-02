CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    product TEXT,
    amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO orders (user_id, product, amount) VALUES
(1, 'Laptop', 1500.00),
(2, 'Mouse', 50.00);
