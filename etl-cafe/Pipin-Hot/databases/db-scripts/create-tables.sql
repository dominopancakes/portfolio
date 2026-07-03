CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY,
    payment_time VARCHAR(16),
    city VARCHAR(58),
    total_price DECIMAL(10,2),
    payment_method  VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS products (
    product_id UUID PRIMARY KEY,
    product_name VARCHAR(80),
    product_price DECIMAL(4,2)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id UUID,
    product_id UUID,
    quantity SMALLINT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)