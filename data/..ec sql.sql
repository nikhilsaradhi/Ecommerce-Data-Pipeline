use ecommerce_data;
CREATE VIEW vw_customer_orders AS
SELECT
    c.customer_id,
    c.customer_city,
    c.customer_state,
    o.order_id,
    o.order_status,
    o.order_purchase_timestamp
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id;

CREATE VIEW vw_order_revenue AS
SELECT
    order_id,
    SUM(price + freight_value) AS total_revenue
FROM order_items
GROUP BY order_id;

CREATE VIEW vw_product_sales AS
SELECT
    product_id,
    COUNT(order_id) AS total_orders,
    SUM(price) AS total_sales
FROM order_items
GROUP BY product_id;

CREATE VIEW vw_seller_performance AS
SELECT
    seller_id,
    COUNT(order_id) AS total_orders,
    SUM(price) AS revenue
FROM order_items
GROUP BY seller_id;

CREATE VIEW vw_payment_analysis AS
SELECT
    payment_type,
    COUNT(order_id) AS total_orders,
    SUM(payment_value) AS total_payment
FROM order_payments
GROUP BY payment_type;

CREATE VIEW vw_review_analysis AS
SELECT
    review_score,
    COUNT(*) AS total_reviews
FROM order_reviews
GROUP BY review_score;

CREATE VIEW vw_delivery_performance AS
SELECT
    order_id,
    DATEDIFF(order_delivered_customer_date,
             order_purchase_timestamp) AS delivery_days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;