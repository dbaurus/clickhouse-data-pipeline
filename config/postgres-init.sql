CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INT,
    product TEXT,
    amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Создаём временный список товаров с диапазонами цен
WITH product_list AS (
    SELECT 'Laptop' AS product, 800.00 AS min_price, 2500.00 AS max_price
    UNION ALL SELECT 'Mouse', 20.00, 100.00
    UNION ALL SELECT 'Keyboard', 50.00, 300.00
    UNION ALL SELECT 'Monitor', 150.00, 800.00
    UNION ALL SELECT 'Headphones', 30.00, 400.00
    UNION ALL SELECT 'Phone', 300.00, 1500.00
    UNION ALL SELECT 'Tablet', 200.00, 1000.00
    UNION ALL SELECT 'USB Cable', 5.00, 25.00
    UNION ALL SELECT 'External SSD', 100.00, 600.00
    UNION ALL SELECT 'Router', 70.00, 300.00
),
random_orders AS (
    SELECT
        s.i,
        (random() * 99 + 1)::int AS user_id,
        (
            -- Принудительно делаем выбор зависимым от строки
            SELECT product
            FROM product_list
            ORDER BY random() * s.i  -- s.i — уникальный индекс строки
            LIMIT 1
        ) AS product_name
    FROM generate_series(1, 10000) AS s(i)
)
-- Вставляем
INSERT INTO orders (user_id, product, amount)
SELECT
    ro.user_id,
    ro.product_name,
    pl.min_price + (random() * (pl.max_price - pl.min_price)) AS amount
FROM random_orders ro
JOIN product_list pl ON pl.product = ro.product_name;
