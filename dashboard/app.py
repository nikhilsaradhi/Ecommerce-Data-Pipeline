
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Ecommerce Analytics Dashboard",
    layout="wide"
)

st.markdown("""
<style>

/* KPI Container */
.kpi-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2E2E2E;
    text-align: center;
}

/* KPI Title */
.kpi-title {
    font-size: 15px;
    font-weight: 700;
    color: #AAAAAA;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}

/* KPI Value */
.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #7b2ff7, #f107a3);
}

.main {
    background: linear-gradient(135deg, #7b2ff7, #f107a3);
}

h1, h2, h3 {
    color: white !important;
    font-weight: bold;
}

div[data-testid="stMetric"] {
    background-color: #ffffff20;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #6a11cb, #2575fc);
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align: center;'> E-COMMERCE ANALYTICS & BUSINESS INSIGHTS</h1>",
    unsafe_allow_html=True
)


daily = pd.DataFrame(requests.get(f"{API_URL}/daily-orders").json())
monthly = pd.DataFrame(requests.get(f"{API_URL}/monthly-orders").json())
top_products = pd.DataFrame(requests.get(f"{API_URL}/top-products").json())
seller_city = pd.DataFrame(requests.get(f"{API_URL}/seller-city").json())
category = pd.DataFrame(requests.get(f"{API_URL}/category-contribution").json())

if not seller_city.empty:
    seller_city["seller_city"] = seller_city["seller_city"].str.title()


st.sidebar.header("Control Panel")

view_mode = st.sidebar.radio("Time View", ["Monthly", "Daily"])
top_n = st.sidebar.slider("Top N Records", 5, 20, 10)

selected_categories = st.sidebar.multiselect(
    "Category Filter",
    options=top_products["product_name"].unique() if not top_products.empty else [],
    default=top_products["product_name"].unique() if not top_products.empty else []
)

selected_cities = st.sidebar.multiselect(
    "Seller City Filter",
    options=seller_city["seller_city"].unique() if not seller_city.empty else [],
    default=seller_city["seller_city"].unique() if not seller_city.empty else []
)


if selected_categories:
    top_products = top_products[top_products["product_name"].isin(selected_categories)]

if selected_cities:
    seller_city = seller_city[seller_city["seller_city"].isin(selected_cities)]

trend_data = monthly if view_mode == "Monthly" else daily
x_axis = "month" if view_mode == "Monthly" else "order_day"


col1, col2, col3 = st.columns(3)

total_orders = int(daily["total_orders"].sum()) if not daily.empty else 0
total_revenue = int(seller_city["revenue"].sum()) if not seller_city.empty else 0
total_categories = len(top_products)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL ORDERS</div>
        <div class="kpi-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL REVENUE</div>
        <div class="kpi-value"> {total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">TOTAL CATEGORIES</div>
        <div class="kpi-value">{total_categories}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()


row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    fig_line = px.line(
        trend_data,
        x=x_axis,
        y="total_orders",
        title="ORDERS TREND",
        markers=True,
        height=380
    )
    fig_line.update_traces(line_color="orange")
    st.plotly_chart(fig_line, use_container_width=True)

with row1_col2:
    fig_area = px.area(
        daily,
        x="order_day",
        y="total_orders",
        height=380,
        title="DAILY GROWTH AREA"
    )
    st.plotly_chart(fig_area, use_container_width=True)

with row1_col3:
    fig_bar_v = px.bar(
        top_products.head(top_n),
        x="product_name",
        y="total_orders",
        title="TOP PRODUCT CATEGORIES",
        color="total_orders",
        height=380,
        color_continuous_scale="Blues"
    )
    fig_bar_v.update_layout(xaxis_tickangle=-30)
    st.plotly_chart(fig_bar_v, use_container_width=True)


row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
         fig_bar_h = px.bar(
        seller_city.head(top_n).sort_values("revenue", ascending=True),
        x="revenue",
        y="seller_city",
        orientation="h",
        title="SELLER'S REVENUE BY CITY",
        color_discrete_sequence=["#4FC3F7"]
    )

         fig_bar_h.update_layout(
        height=380,
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        template="plotly_dark"
    )

         st.plotly_chart(fig_bar_h, use_container_width=True)

with row2_col2:
    fig_pie = px.pie(
        category.head(6),
        names="product_name",
        values="total_orders",
        hole=0.5,
        height=380,
        title="CATEGORY CONTRIBUTION"
    )
    fig_pie.update_traces(textposition="outside",textinfo="percent+label")
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with row2_col3:
    fig_hist = px.histogram(
        daily,
        x="total_orders",
        nbins=20,
        height=380,
        title="ORDERS DISTRIBUTION"
    )
    st.plotly_chart(fig_hist, use_container_width=True)