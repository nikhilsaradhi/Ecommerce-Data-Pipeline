use ecommerce_data;
CREATE TABLE customer_sales_mart AS
SELECT
    c.customer_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.price) AS total_product_value,
    SUM(oi.freight_value) AS total_freight,
    SUM(oi.price + oi.freight_value) AS total_spent
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_items oi
    ON o.order_id = oi.order_id
GROUP BY c.customer_id;

CREATE TABLE product_performance_mart AS
SELECT
    p.product_id,
    p.product_category_name,
    COUNT(oi.order_id) AS total_orders,
    SUM(oi.price) AS total_revenue,
    AVG(r.review_score) AS avg_review_score
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
LEFT JOIN order_reviews r
    ON oi.order_id = r.order_id
GROUP BY p.product_id, p.product_category_name;

CREATE TABLE seller_performance_mart AS
SELECT
    s.seller_id,
    COUNT(oi.order_id) AS total_orders,
    SUM(oi.price) AS seller_revenue,
    AVG(r.review_score) AS avg_rating
FROM sellers s
JOIN order_items oi
    ON s.seller_id = oi.seller_id
LEFT JOIN order_reviews r
    ON oi.order_id = r.order_id
GROUP BY s.seller_id;

CREATE TABLE order_revenue_mart AS
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    SUM(oi.price) AS order_value,
    SUM(oi.freight_value) AS freight_cost,
    SUM(op.payment_value) AS payment_value
FROM orders o
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN order_payments op
    ON o.order_id = op.order_id
GROUP BY o.order_id, o.order_purchase_timestamp;

show tables;
CREATE TABLE ecommerce_events (
    event_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    event_type VARCHAR(50),
    product_id VARCHAR(50),
    event_timestamp TIMESTAMP,
    platform VARCHAR(20)
);

drop table ecommerce_events;

CREATE TABLE ecommerce_events (

    event_id VARCHAR(50) PRIMARY KEY,

    event_type VARCHAR(50),

    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    order_id VARCHAR(50),

    event_timestamp DATETIME,

    device VARCHAR(20),
    city VARCHAR(100),
    country VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE ecommerce_events
ADD CONSTRAINT fk_event_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id);

ALTER TABLE ecommerce_events
ADD CONSTRAINT fk_event_product
FOREIGN KEY (product_id)
REFERENCES products(product_id);

ALTER TABLE ecommerce_events
ADD CONSTRAINT fk_event_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id);

CREATE INDEX idx_event_time
ON ecommerce_events(event_timestamp);

CREATE INDEX idx_event_type
ON ecommerce_events(event_type);

CREATE INDEX idx_customer_event
ON ecommerce_events(customer_id);

SELECT COUNT(*) FROM ecommerce_events;

CREATE VIEW vw_user_activity AS
SELECT
    customer_id,
    COUNT(*) total_events
FROM ecommerce_events
GROUP BY customer_id;

CREATE VIEW vw_event_distribution AS
SELECT
    event_type,
    COUNT(*) total
FROM ecommerce_events
GROUP BY event_type;

CREATE VIEW vw_product_views AS
SELECT
    product_id,
    COUNT(*) views
FROM ecommerce_events
WHERE event_type='product_view'
GROUP BY product_id;

CREATE VIEW vw_add_to_cart AS
SELECT
    product_id,
    COUNT(*) cart_count
FROM ecommerce_events
WHERE event_type='add_to_cart'
GROUP BY product_id;

CREATE VIEW vw_purchase_events AS
SELECT
    product_id,
    COUNT(*) purchases
FROM ecommerce_events
WHERE event_type='purchase'
GROUP BY product_id;

CREATE VIEW vw_conversion_funnel AS
SELECT
    customer_id,
    SUM(event_type='product_view') views,
    SUM(event_type='add_to_cart') carts,
    SUM(event_type='purchase') purchases
FROM ecommerce_events
GROUP BY customer_id;

CREATE VIEW vw_hourly_events AS
SELECT
    HOUR(event_timestamp) event_hour,
    COUNT(*) total_events
FROM ecommerce_events
GROUP BY event_hour;



CREATE VIEW vw_daily_events AS
SELECT
    DATE(event_timestamp) event_date,
    COUNT(*) total_events
FROM ecommerce_events
GROUP BY event_date;

CREATE TABLE dim_customers AS
SELECT DISTINCT
    customer_id,
    customer_city,
    customer_state
FROM customers;

CREATE TABLE dim_products AS
SELECT DISTINCT
    product_id,
    product_category_name
FROM products;

CREATE TABLE dim_sellers AS
SELECT DISTINCT
    seller_id,
    seller_city,
    seller_state
FROM sellers;

CREATE TABLE dim_date AS
SELECT DISTINCT
    DATE(order_purchase_timestamp) AS order_date,
    YEAR(order_purchase_timestamp) AS year,
    MONTH(order_purchase_timestamp) AS month,
    DAY(order_purchase_timestamp) AS day
FROM orders;

CREATE TABLE dim_geolocation AS
SELECT DISTINCT
    geolocation_zip_code_prefix,
    geolocation_city,
    geolocation_state
FROM geolocation;

CREATE TABLE fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    oi.product_id,
    oi.seller_id,
    DATE(o.order_purchase_timestamp) AS order_date,
    oi.price,
    oi.freight_value
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id;

CREATE TABLE fact_payments AS
SELECT
    order_id,
    payment_type,
    payment_installments,
    payment_value
FROM order_payments;

CREATE TABLE fact_reviews AS
SELECT
    order_id,
    review_score
FROM order_reviews;

CREATE TABLE fact_events AS
SELECT
    event_id,
    event_type,
    customer_id,
    product_id,
    order_id,
    event_timestamp
FROM ecommerce_events;

show tables;

drop table dim_geolocation;
