-- FACT TABLE

CREATE OR REPLACE TABLE ecommerce_dw.fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    p.payment_type,
    p.payment_value,
    r.review_score
FROM ecommerce_dw.clean_orders o
LEFT JOIN ecommerce_dw.clean_order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN ecommerce_dw.clean_payments p
    ON o.order_id = p.order_id
LEFT JOIN ecommerce_dw.clean_reviews r
    ON o.order_id = r.order_id;




CREATE OR REPLACE TABLE ecommerce_dw.dim_customers AS
SELECT DISTINCT
    customer_id,
    customer_city,
    customer_state
FROM ecommerce_dw.clean_customers;


CREATE OR REPLACE TABLE ecommerce_dw.dim_products AS
SELECT DISTINCT
    product_id,
    product_category_name,
    product_category_name_english
FROM ecommerce_dw.clean_products;


CREATE OR REPLACE TABLE ecommerce_dw.dim_sellers AS
SELECT DISTINCT
    seller_id,
    seller_city,
    seller_state
FROM ecommerce_dw.clean_sellers;