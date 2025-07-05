import streamlit as st
import requests
import pandas as pd

BASE_URL = "https://expense-buddy-mcp-server.onrender.com"


st.set_page_config(page_title="💸 Expense Buddy", layout="wide")
st.title("💸 Expense & Budget Buddy")

# ----------------------------
# ✅ SESSION STATE for messages
# ----------------------------
if "log_message" not in st.session_state:
    st.session_state.log_message = ""
if "budget_message" not in st.session_state:
    st.session_state.budget_message = ""
if "current_budget_message" not in st.session_state:
    st.session_state.current_budget_message = ""

# ----------------------------
# 📊 Sidebar: Weekly Overview + Reset
# ----------------------------
with st.sidebar:
    st.header("📅 Weekly Overview")

    try:
        trends_res = requests.get(f"{BASE_URL}/expense/trends")
        trends = trends_res.json()

        spent = trends["weekly_total"]
        budget = trends["weekly_budget"]
        remaining = max(budget - spent, 0)

        st.metric("Weekly Budget", f"₹{budget:.2f}")
        st.metric("Total Spent", f"₹{spent:.2f}")
        st.metric("Remaining", f"₹{remaining:.2f}")

        st.write("### 📂 Top Categories")
        for category, amt in trends["categories"].items():
            st.write(f"- {category}: ₹{amt:.2f}")

        progress = min(spent / budget, 1.0) if budget else 0
        st.progress(progress)

    except Exception as e:
        st.warning(f"Could not load summary: {e}")

    st.write("---")
    if st.button("🗑️ Reset All Expenses"):
        res = requests.post(f"{BASE_URL}/expenses/reset")
        st.session_state.log_message = res.json().get("status", "Something went wrong!")
        st.rerun()

# ----------------------------
# 📌 Log a new expense
# ----------------------------
st.header("📌 Log a new expense")

# ✅ Show log message
if st.session_state.log_message:
    st.success(st.session_state.log_message)
    st.session_state.log_message = ""  # clear after showing

with st.form("expense_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date")
        amount = st.number_input("Amount", min_value=0.0)
    with col2:
        category = st.text_input("Category (or leave blank for auto)")
        note = st.text_input("Note")

    submitted = st.form_submit_button("Log Expense")

if submitted:
    expense = {
        "date": str(date),
        "amount": amount,
        "category": category,
        "note": note
    }
    res = requests.post(f"{BASE_URL}/expense", json=expense)
    data = res.json()
    st.session_state.log_message = data.get("status", f"Unexpected response: {data}")
    st.rerun()

# ----------------------------
# 📊 Expense Trends + Charts
# ----------------------------
# ----------------------------
# 📊 Expense Trends + Charts
# ----------------------------
st.header("📊 Expense Trends")

with st.expander("Click to view Expense Trends"):
    res = requests.get(f"{BASE_URL}/expense/trends")
    data = res.json()

    st.subheader("📅 Daily Totals")
    st.bar_chart(pd.Series(data["daily_totals"]))

    st.subheader("📂 Spending by Category")
    st.bar_chart(pd.Series(data["categories"]))

    st.json(data)


# ----------------------------
# 💡 Saving Tip
# ----------------------------
st.header("💡 Saving Tip")

if st.button("Get Tip"):
    data = requests.get(f"{BASE_URL}/expense/tip").json()
    if "tip" in data:
        st.info(data["tip"])
    if "streak" in data:
        st.success(data["streak"])

# ----------------------------
# 📅 Weekly Budget
# ----------------------------
st.header("💰 Weekly Budget Settings")

# ✅ Show budget messages
if st.session_state.budget_message:
    st.success(st.session_state.budget_message)
    st.session_state.budget_message = ""

if st.session_state.current_budget_message:
    st.info(st.session_state.current_budget_message)
    st.session_state.current_budget_message = ""

budget = st.number_input("Set new weekly budget", min_value=0.0)

if st.button("Update Budget"):
    res = requests.post(f"{BASE_URL}/budget", json={"weekly_budget": budget})
    st.session_state.budget_message = f"Budget updated: ₹{res.json()['weekly_budget']}"
    st.rerun()

if st.button("Get Current Budget"):
    res = requests.get(f"{BASE_URL}/budget")
    st.session_state.current_budget_message = f"Weekly Budget: ₹{res.json()['weekly_budget']}"
    st.rerun()

# ----------------------------
# 📤 Export Expenses
# ----------------------------
st.header("📤 Export Expenses")

if st.button("Export to CSV"):
    res = requests.get(f"{BASE_URL}/expenses/export")
    csv_data = res.text
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="expenses.csv",
        mime="text/csv"
    )
