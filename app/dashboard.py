from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="E-commerce Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "ecommerce.db"


@st.cache_data
def load_data() -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM delivered_sales"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["year_month"] = df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
    df["delivery_status"] = df["estimated_vs_actual_diff_days"].apply(
        lambda x: "Late" if x > 0 else "On time / Early"
    )
    return df


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_number(value: float) -> str:
    return f"{value:,.0f}"


df = load_data()

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(180deg, #f5f7fb 0%, #ffffff 100%);
    }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
        padding: 28px 32px;
        border-radius: 22px;
        color: white;
        margin-bottom: 18px;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
    }
    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 2.2rem;
    }
    .hero p {
        margin: 0;
        font-size: 1rem;
        opacity: 0.92;
    }
    .insight-box {
        background: #eef6ff;
        border-left: 6px solid #2563eb;
        padding: 16px 18px;
        border-radius: 14px;
        margin: 8px 0 18px 0;
        color: #0f172a;
    }
    .insight-box strong {
        color: #0b3b91;
    }
    .section-title {
        margin-top: 10px;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>E-commerce Sales Dashboard</h1>
        <p>Interactive business analysis of delivered orders from the Olist dataset.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Filters")
    available_years = sorted(df["purchase_year"].dropna().unique().tolist())
    selected_years = st.multiselect(
        "Purchase Year",
        options=available_years,
        default=available_years,
    )

    available_states = sorted(df["customer_state"].dropna().unique().tolist())
    selected_states = st.multiselect(
        "Customer State",
        options=available_states,
        default=available_states,
    )

    show_late_only = st.checkbox("Show late deliveries only", value=False)

filtered_df = df[
    df["purchase_year"].isin(selected_years) & df["customer_state"].isin(selected_states)
].copy()

if show_late_only:
    filtered_df = filtered_df[filtered_df["delivery_status"] == "Late"].copy()

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

total_revenue = filtered_df["total_order_value"].sum()
total_orders = filtered_df["order_id"].nunique()
unique_customers = filtered_df["customer_unique_id"].nunique()
avg_order_value = filtered_df["total_order_value"].mean()
avg_review_score = filtered_df["review_score_mean"].mean()
late_delivery_rate = (filtered_df["estimated_vs_actual_diff_days"] > 0).mean() * 100

st.markdown("### Executive KPIs")
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

col1.metric("Total Revenue", format_currency(total_revenue))
col2.metric("Total Orders", format_number(total_orders))
col3.metric("Unique Customers", format_number(unique_customers))
col4.metric("Average Order Value", f"${avg_order_value:,.2f}")
col5.metric("Average Review Score", f"{avg_review_score:.2f}")
col6.metric("Late Delivery Rate", f"{late_delivery_rate:.2f}%")

monthly_sales = (
    filtered_df.groupby("year_month", as_index=False)
    .agg(
        monthly_revenue=("total_order_value", "sum"),
        monthly_orders=("order_id", "count"),
        avg_order_value=("total_order_value", "mean"),
    )
    .sort_values("year_month")
)

state_sales = (
    filtered_df.groupby("customer_state", as_index=False)
    .agg(
        total_revenue=("total_order_value", "sum"),
        total_orders=("order_id", "count"),
        avg_order_value=("total_order_value", "mean"),
    )
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

city_sales = (
    filtered_df.groupby("customer_city", as_index=False)
    .agg(
        total_revenue=("total_order_value", "sum"),
        total_orders=("order_id", "count"),
    )
    .sort_values("total_revenue", ascending=False)
    .head(10)
)

review_by_delivery = (
    filtered_df.groupby("delivery_status", as_index=False)
    .agg(
        avg_review_score=("review_score_mean", "mean"),
        avg_delivery_delay=("delivery_delay_days", "mean"),
        n_orders=("order_id", "count"),
    )
)

best_state = state_sales.iloc[0]
on_time_score = review_by_delivery.loc[
    review_by_delivery["delivery_status"] == "On time / Early", "avg_review_score"
]
late_score = review_by_delivery.loc[
    review_by_delivery["delivery_status"] == "Late", "avg_review_score"
]

if not on_time_score.empty and not late_score.empty:
    score_gap = on_time_score.iloc[0] - late_score.iloc[0]
    insight_text = (
        f"Customer satisfaction drops by {score_gap:.2f} points when deliveries are late. "
        f"The top state by revenue in the current view is {best_state['customer_state']} "
        f"with {format_currency(best_state['total_revenue'])} in sales."
    )
else:
    insight_text = (
        f"The top state by revenue in the current view is {best_state['customer_state']} "
        f"with {format_currency(best_state['total_revenue'])} in sales."
    )

st.markdown(
    f"""
    <div class="insight-box">
        <strong>Key Insight</strong><br>
        {insight_text}
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns((1.7, 1))

with left_col:
    st.markdown("### Revenue and Demand Trends")
    st.line_chart(
        monthly_sales.set_index("year_month")[["monthly_revenue", "monthly_orders"]],
        use_container_width=True,
    )

    trend_table = monthly_sales.copy()
    trend_table["monthly_revenue"] = trend_table["monthly_revenue"].round(2)
    trend_table["avg_order_value"] = trend_table["avg_order_value"].round(2)
    st.dataframe(trend_table, use_container_width=True, hide_index=True)

with right_col:
    st.markdown("### Delivery and Experience")
    review_display = review_by_delivery.copy()
    review_display["avg_review_score"] = review_display["avg_review_score"].round(2)
    review_display["avg_delivery_delay"] = review_display["avg_delivery_delay"].round(2)
    st.dataframe(review_display, use_container_width=True, hide_index=True)

    st.markdown("### Order Value Distribution")
    st.bar_chart(
        filtered_df["total_order_value"]
        .dropna()
        .clip(upper=filtered_df["total_order_value"].quantile(0.95))
        .reset_index(drop=True)
        .head(200),
        use_container_width=True,
    )

geo_col1, geo_col2 = st.columns(2)

with geo_col1:
    st.markdown("### Top States by Revenue")
    state_display = state_sales.copy()
    state_display["total_revenue"] = state_display["total_revenue"].round(2)
    state_display["avg_order_value"] = state_display["avg_order_value"].round(2)
    st.dataframe(state_display, use_container_width=True, hide_index=True)

with geo_col2:
    st.markdown("### Top Cities by Revenue")
    city_display = city_sales.copy()
    city_display["total_revenue"] = city_display["total_revenue"].round(2)
    st.dataframe(city_display, use_container_width=True, hide_index=True)

st.caption(
    "Data source: Olist Brazilian E-Commerce Public Dataset. "
    "Dashboard scope: delivered orders only."
)
