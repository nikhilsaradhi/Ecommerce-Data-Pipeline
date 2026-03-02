# 🚀 Event-Driven E-Commerce Data Pipeline & Analytics Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![BigQuery](https://img.shields.io/badge/BigQuery-Cloud%20Warehouse-yellow)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 Project Overview

This project implements a **modern event-driven e-commerce data pipeline** that simulates real-world enterprise analytics architecture.

It captures transactional & behavioral events, processes them using ETL, models them using Star Schema, loads them into BigQuery, exposes data via FastAPI, and visualizes insights through an interactive Streamlit dashboard.

---

## 🎯 Main Objectives

- Build an end-to-end data pipeline
- Implement event-driven architecture
- Perform ETL cleaning & validation
- Design fact & dimension tables
- Create cloud-based analytical warehouse
- Develop REST APIs
- Build a BI-style dashboard

---

# 🏗 Architecture Diagram

```
Raw CSV Data
     ↓
MySQL (Raw Tables)
     ↓
Python ETL Cleaning
     ↓
MySQL (Clean Tables)
     ↓
Star Schema (Fact & Dimension Tables)
     ↓
Google BigQuery
     ↓
Analytical Views
     ↓
FastAPI (REST APIs)
     ↓
Streamlit Dashboard
```

---

# ⚡ Event-Driven System

### Generated Events

- page_view  
- product_view  
- add_to_cart  
- remove_from_cart  
- checkout_started  
- payment_success  
- payment_failed  
- order_cancelled  
- order_delivered  
- review_submitted  

### Why Event-Driven?

Modern companies use event-driven systems to:

- Track user behavior
- Monitor conversion funnels
- Analyze real-time performance
- Optimize business decisions

This project simulates enterprise-grade clickstream tracking.

---

# 🧱 Data Modeling (Star Schema)

## ⭐ Fact Table

### `fact_orders`

| Column | Description |
|--------|-------------|
| order_id | Unique order |
| customer_id | Buyer reference |
| product_id | Product reference |
| order_date | Purchase date |
| price | Product price |
| freight_value | Shipping cost |

Fact tables store measurable metrics.

---

## 📐 Dimension Tables

- dim_customers
- dim_products
- dim_sellers
- dim_date

Dimension tables provide descriptive context.

Fact = Numbers  
Dimension = Description  

---

# 📊 Analytical Views (BigQuery)

- daily_orders  
- monthly_orders  
- top_products  
- seller_revenue_city  
- category_contribution  
- orders_distribution  

These views provide business-ready datasets.

---

# 🔌 FastAPI Layer

FastAPI exposes analytics as REST endpoints.

### API Endpoints

- `/daily-orders`
- `/monthly-orders`
- `/top-products`
- `/seller-city`
- `/category-contribution`

Benefits:

- Scalable backend
- Decoupled architecture
- Production-ready structure

---

# 📈 Streamlit Dashboard

### KPIs

- Total Orders
- Total Revenue
- Active Categories
- Revenue Growth %

### Visualizations

- 📈 Line Chart → Order Volume Over Time  
- 🌊 Area Chart → Cumulative Order Growth  
- 📊 Vertical Bar → Top Product Categories  
- 🏙 Horizontal Bar → Seller Revenue by City  
- 🥧 Donut Chart → Category Sales Contribution  
- 📦 Histogram → Order Volume Distribution  

### Features

- Global Time Filter (Daily / Monthly)
- Top N Filter
- Professional Dark Theme
- Responsive Layout

---

# 📷 Dashboard Screenshots

_Add screenshots here_

```
![Dashboard Overview](screenshots/dashboard_overview.png)
![Category Analysis](screenshots/category_analysis.png)
![Seller Revenue](screenshots/seller_revenue.png)
```

---

# 🛠 Tech Stack

- Python
- Pandas
- Plotly
- Streamlit
- FastAPI
- MySQL
- Google BigQuery
- SQLAlchemy
- Faker

---

# ⚙️ How to Run

## 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 2️⃣ Start FastAPI

```bash
uvicorn main:app --reload
```

## 3️⃣ Run Streamlit

```bash
streamlit run dashboard/app.py
```

---

# 🌍 Real-World Applications

Used in:

- E-Commerce Platforms
- Retail Analytics
- Banking Systems
- Clickstream Analytics
- SaaS Analytics

Companies using similar systems:

Amazon • Flipkart • Netflix • Walmart • Shopify

---

# 🚀 Deployment Options

- Render
- Railway
- Google Cloud Run
- AWS EC2
- Streamlit Cloud

---

# 🎓 Resume Description

Built a production-style event-driven e-commerce data pipeline using MySQL, BigQuery, FastAPI, and Streamlit. Implemented ETL processing, star schema modeling, cloud warehousing, REST APIs, and an interactive BI dashboard to simulate enterprise-grade analytics architecture.

---

# 📌 Project Status

✅ Completed  
✅ Cloud Integrated  
✅ Event-Driven Architecture  
✅ Full Analytics Stack Implemented  

---

# 👨‍💻 Author

Developed as part of a Data Engineering & Business Intelligence Portfolio Project.
