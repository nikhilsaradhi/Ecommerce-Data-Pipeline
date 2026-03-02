import streamlit as st
import requests
import pandas as pd
import plotly.express as px



API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)



st.markdown("""
<style>
.stApp { background-color: #0E1117; color: white; }

.kpi-card {
    background-color: #FFF8DC;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2E2E2E;
    text-align: center;
}

.kpi-title {
    font-size: 28px;
    font-weight: 800;
    color: #000000;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center; color: orange; font-size: 35px;'>EVENT DATA DRIVEN E-COMMERCE ANALYTICS DASHBOARD</h1>",
    unsafe_allow_html=True
)

 
st.markdown("""
<style>

/* Sidebar Background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
    padding-top: 25px;
}

/* Sidebar Container Padding */
section[data-testid="stSidebar"] > div {
    padding: 20px 18px;
}

/* Sidebar Title */
.sidebar-title {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Section Header */
.sidebar-section {
    font-size: 20px;
    font-weight: 700;
    color: #94a3b8;
    margin-top: 25px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* Divider */
.sidebar-divider {
    border-top: 1px solid #1f2937;
    margin: 20px 0;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #1e293b !important;
    border-radius: 8px !important;
    border: 1px solid #334155 !important;
}

/* Slider Track */
div[data-testid="stSlider"] > div > div {
    color: #38bdf8 !important;
}

/* Label Styling */
label {
    font-weight: 600 !important;
    color: #e2e8f0 !important;
}

/* Remove Streamlit Menu & Footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)



with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚙️ Control Panel</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-section">Time View</div>', unsafe_allow_html=True)
    view_mode = st.radio(
        "",
        ["Monthly", "Daily"],
        horizontal=False
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Top N Records</div>', unsafe_allow_html=True)
    top_n = st.slider(
        "",
        min_value=5,
        max_value=20,
        value=10
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.caption("")


def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return pd.DataFrame(data)
        return pd.DataFrame()
    except:
        return pd.DataFrame()



trend_data = fetch_data(f"orders?view={view_mode.lower()}")
top_products = fetch_data(f"top-products?top_n={top_n}")
seller_city = fetch_data(f"seller-city?top_n={top_n}")
category = fetch_data("category-contribution?top_n=6")

x_axis = "month" if view_mode == "Monthly" else "order_day"



col1, col2, col3 = st.columns(3)

if not trend_data.empty and x_axis in trend_data.columns:

    trend_data = trend_data.sort_values(x_axis)

    
has_orders = "total_orders" in trend_data.columns
has_revenue = "total_revenue" in trend_data.columns

total_orders = int(trend_data["total_orders"].sum()) if has_orders else 0
total_revenue = int(seller_city["revenue"].sum()) if not seller_city.empty else 0
total_categories = category["product_name"].nunique() if not category.empty else 0


if has_revenue and len(trend_data) > 1:
    prev = trend_data["total_revenue"].iloc[-2]
    curr = trend_data["total_revenue"].iloc[-1]
    growth = ((curr - prev) / prev) * 100 if prev != 0 else 0
else:
    growth = 0

arrow = "▲" if growth >= 0 else "▼"
arrow_color = "green" if growth >= 0 else "red"
total_categories = len(category) if not category.empty else 0

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
        <div class="kpi-value">₹ {total_revenue:,.0f}</div>
        <div style=" font-weight:600;">
            
        
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">ACTIVE CATEGORIES</div>
        <div class="kpi-value">{total_categories}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()



if not trend_data.empty and x_axis in trend_data.columns:

    

    
 row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    fig1 = px.line(
        trend_data,
        x=x_axis,
        y="total_orders",
        height=360,
        template="plotly_dark"
    )

    fig1.update_traces(
        line=dict(width=3, color="#3B82F6"),
        mode="lines+markers",
        marker=dict(size=5)
    )

    fig1.update_layout(
        title=dict(text="ORDERS TREND", font_size=30, x=0.02),
        margin=dict(l=20, r=20, t=45, b=20),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117"
    )

    st.plotly_chart(fig1, use_container_width=True)


with row1_col2:
    fig2 = px.area(
        trend_data,
        x=x_axis,
        y="total_orders",
        height=360,
        template="plotly_dark"
    )

    fig2.update_traces(
        line=dict(width=2, color="#06B6D4"),
        fillcolor="rgba(6,182,212,0.25)"
    )

    fig2.update_layout(
        title=dict(text="ORDER GROWTH AREA", font_size=30, x=0.02),
        margin=dict(l=20, r=20, t=45, b=20),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117"
    )

    st.plotly_chart(fig2, use_container_width=True)


with row1_col3:
    if not top_products.empty:
        fig3 = px.bar(
            top_products,
            x="product_name",
            y="total_orders",
            height=360,
            template="plotly_dark"
        )

        fig3.update_traces(
            marker_color="#800080"
        )

        fig3.update_layout(
            title=dict(text="TOP PRODUCTS", font_size=30, x=0.02),
            xaxis_tickangle=-30,
            margin=dict(l=20, r=20, t=45, b=20),
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117"
        )

        st.plotly_chart(fig3, use_container_width=True)



row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    if not seller_city.empty:
        fig4 = px.bar(
            seller_city.sort_values("revenue"),
            x="revenue",
            y="seller_city",
            orientation="h",
            height=360,
            template="plotly_dark"
        )

        fig4.update_traces(marker_color="#40E0D0")

        fig4.update_layout(
            title=dict(text="SELLER REVENUE BY CITY", font_size=30, x=0.02),
            margin=dict(l=20, r=20, t=45, b=20),
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117"
        )

        st.plotly_chart(fig4, use_container_width=True)


with row2_col2:
    if not category.empty:
        fig5 = px.pie(
            category,
            names="product_name",
            values="total_orders",
            hole=0.55,
            height=360,
            template="plotly_dark"
        )

        fig5.update_traces(textinfo="percent",textposition="outside")

        fig5.update_layout(
            title=dict(text="CATEGORY CONTRIBUTION", font_size=30, x=0.02),
            margin=dict(l=20, r=20, t=45, b=20),
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117"
        )

        st.plotly_chart(fig5, use_container_width=True)


with row2_col3:
    fig6 = px.histogram(
        trend_data,
        x="total_orders",
        nbins=20,
        height=360,
        template="plotly_dark"
    )

    fig6.update_traces(marker_color="#FFFF00")

    fig6.update_layout(
        title=dict(text="ORDERS DISTRIBUTION", font_size=30, x=0.02),
        margin=dict(l=20, r=20, t=45, b=20),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117"
    )

    st.plotly_chart(fig6, use_container_width=True)