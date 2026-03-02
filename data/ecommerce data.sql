CREATE DATABASE  ecommerce_data;
USE ecommerce_data;

CREATE TABLE customers (
    customer_id VARCHAR(50),
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(5)
);

CREATE TABLE orders (
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    order_status VARCHAR(50),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2)
);

CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(50),
    payment_installments INT,
    payment_value DECIMAL(10,2)
);

CREATE TABLE products (
    product_id VARCHAR(50),
    product_category_name VARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

CREATE TABLE order_reviews (
    review_id VARCHAR(50),
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME
);

CREATE TABLE sellers (
    seller_id VARCHAR(50),
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(5)
);

CREATE TABLE geolocation (
    geolocation_zip_code_prefix INT,
    geolocation_lat DECIMAL(10,7),
    geolocation_lng DECIMAL(10,7),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(5)
);

CREATE TABLE category_translation (
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100)
);

show tables;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE order_reviews;
TRUNCATE TABLE order_payments;
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
TRUNCATE TABLE products;
TRUNCATE TABLE sellers;
TRUNCATE TABLE customers;
TRUNCATE TABLE geolocation;
TRUNCATE TABLE product_category_name_translation;
SET FOREIGN_KEY_CHECKS = 1;
TRUNCATE TABLE product_category_name_translation;



drop table category_translation;
show tables;
show databases;
select count(*) from customers;
select count(*) from orders;
select count(*) from order_items;
select count(*) from order_payments;
select count(*) from product_category_name_translation;
select count(*) from products;
select count(*) from sellers;
select count(*) from geolocation;
select count(*) from order_reviews;

show create table customers;
ALTER TABLE customers ADD PRIMARY KEY (customer_id);
ALTER TABLE sellers ADD PRIMARY KEY (seller_id);
ALTER TABLE products ADD PRIMARY KEY (product_id);
ALTER TABLE orders ADD PRIMARY KEY (order_id);
ALTER TABLE order_reviews ADD PRIMARY KEY (review_id);

ALTER TABLE order_items 
ADD PRIMARY KEY (order_id, order_item_id);

ALTER TABLE order_payments 
ADD PRIMARY KEY (order_id, payment_sequential);
SELECT COUNT(*) FROM order_reviews;
SELECT COUNT(DISTINCT review_id) FROM order_reviews;
SELECT review_id, COUNT(*) AS cnt
FROM order_reviews
GROUP BY review_id
HAVING cnt > 1;
SELECT review_id, COUNT(*) 
FROM order_reviews
WHERE review_id = '1f97f75959fdde611d52fde0a4ef310c'
GROUP BY review_id;
CREATE TABLE order_reviews_clean AS
select *
FROM (
    SELECT *
    FROM order_reviews
    GROUP BY review_id
) t;

SELECT review_id, COUNT(*) AS cnt
FROM order_reviews
GROUP BY review_id
HAVING cnt > 1;

DELETE FROM order_reviews
WHERE review_id IN (
    SELECT review_id FROM (
        SELECT review_id,
               ROW_NUMBER() OVER (
                   PARTITION BY review_id
                   ORDER BY review_creation_date
               ) AS rn
        FROM order_reviews
    ) t
    WHERE t.rn > 1
);

DELETE FROM order_reviews
WHERE review_id IN (
    SELECT review_id FROM (
        SELECT review_id,
               ROW_NUMBER() OVER (
                   PARTITION BY review_id
                   ORDER BY review_creation_date
               ) AS rn
        FROM order_reviews
    ) t
    WHERE t.rn > 1
);

SELECT COUNT(*) FROM order_reviews;
SELECT COUNT(DISTINCT review_id) FROM order_reviews;
ALTER TABLE order_reviews
ADD PRIMARY KEY (review_id);

ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id);

ALTER TABLE order_items
ADD CONSTRAINT fk_items_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id);

ALTER TABLE order_items
ADD CONSTRAINT fk_items_product
FOREIGN KEY (product_id)
REFERENCES products(product_id);

ALTER TABLE order_items
ADD CONSTRAINT fk_items_seller
FOREIGN KEY (seller_id)
REFERENCES sellers(seller_id);

ALTER TABLE order_payments
ADD CONSTRAINT fk_payments_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id);

ALTER TABLE order_reviews
ADD CONSTRAINT fk_reviews_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id);
desc order_reviews;

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orderitems_product ON order_items(product_id);
CREATE INDEX idx_orderitems_seller ON order_items(seller_id);
CREATE INDEX idx_payments_order ON order_payments(order_id);

desc customers;
desc geolocation;

SELECT *
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
