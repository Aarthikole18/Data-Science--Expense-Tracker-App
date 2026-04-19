import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker", layout="wide")

# Title
st.title("💰 Expense Tracker Dashboard")

# -----------------------------
# 📂 FILE UPLOAD (UPGRADE)
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload your Expense CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/cleaned_expenses.csv")

# Preprocessing
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Month_Num'] = df['Date'].dt.month

# -----------------------------
# 🔍 FILTERS
# -----------------------------
st.sidebar.header("Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

type_filter = st.sidebar.selectbox(
    "Select Type",
    ["All", "Expense", "Income"]
)

filtered_df = df[df['Category'].isin(category_filter)]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df['Type'] == type_filter]

# -----------------------------
# 📊 KPI SECTION
# -----------------------------
total_expense = filtered_df[filtered_df['Type'] == 'Expense']['Amount'].sum()
total_income = filtered_df[filtered_df['Type'] == 'Income']['Amount'].sum()

col1, col2 = st.columns(2)

col1.metric("💸 Total Expense", f"₹{total_expense}")
col2.metric("💰 Total Income", f"₹{total_income}")

# -----------------------------
# 📊 CATEGORY CHART
# -----------------------------
st.subheader("📊 Category-wise Spending")

category_data = filtered_df.groupby('Category')['Amount'].sum()
st.bar_chart(category_data)

# -----------------------------
# 📈 MONTHLY TREND
# -----------------------------
st.subheader("📈 Monthly Trend")

monthly_data = filtered_df.groupby('Month_Num')['Amount'].sum()
st.line_chart(monthly_data)

# -----------------------------
# 🥧 PIE CHART
# -----------------------------
if type_filter == "Expense":
    st.subheader("🥧 Expense Distribution")

    pie_data = filtered_df.groupby('Category')['Amount'].sum()

    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
    ax.axis('equal')

    st.pyplot(fig)

# -----------------------------
# 🧠 INSIGHTS
# -----------------------------
st.subheader("🧠 Insights")

if total_expense > total_income:
    st.error("⚠️ You are overspending!")
else:
    st.success("✅ You are saving money!")

top_category = filtered_df.groupby('Category')['Amount'].sum().idxmax()
st.write(f"🔥 Highest Spending Category: {top_category}")