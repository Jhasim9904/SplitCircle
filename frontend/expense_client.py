import streamlit as st
import requests
import pandas as pd

# 👉 Local dev URL
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="💸 Expense Buddy", layout="wide")
st.title("💸 Expense & Budget Buddy")

# ----------------------------------------
# 🔑 User ID input for per-user JSON files
# ----------------------------------------
st.sidebar.write("🔑 **User ID** (to keep your expenses separate)")
user_id = st.sidebar.text_input("Enter your user ID:", value="demo_user")

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
        trends_res = requests.get(f"{BASE_URL}/expense/trends", params={"user_id": user_id}, timeout=10)
        trends = trends_res.json() if trends_res.status_code == 200 else {}

        spent = trends.get("weekly_total", 0)
        budget = trends.get("weekly_budget", 0)
        remaining = max(budget - spent, 0)

        st.metric("Weekly Budget", f"₹{budget:.2f}")
        st.metric("Total Spent", f"₹{spent:.2f}")
        st.metric("Remaining", f"₹{remaining:.2f}")

        st.write("### 📂 Top Categories")
        for category, amt in trends.get("categories", {}).items():
            st.write(f"- {category}: ₹{amt:.2f}")

        progress = min(spent / budget, 1.0) if budget else 0
        st.progress(progress)

    except Exception as e:
        st.warning(f"Could not load summary: {e}")

    st.write("---")
    if st.button("🗑️ Reset All Expenses"):
        try:
            res = requests.post(f"{BASE_URL}/expenses/reset", params={"user_id": user_id}, timeout=10)
            status = res.json().get("status", "Something went wrong!")
            st.session_state.log_message = status
        except Exception as e:
            st.session_state.log_message = f"Error resetting: {e}"
        st.rerun()

# ----------------------------
# 📌 Log a new expense
# ----------------------------
st.header("📌 Log a new expense")

if st.session_state.log_message:
    st.success(st.session_state.log_message)
    st.session_state.log_message = ""

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
    try:
        res = requests.post(f"{BASE_URL}/expense", json=expense, params={"user_id": user_id}, timeout=10)
        if res.status_code == 200:
            data = res.json()
            st.session_state.log_message = data.get("status", "Expense logged!")
        else:
            st.session_state.log_message = f"Error: {res.status_code}"
    except Exception as e:
        st.session_state.log_message = f"Request failed: {e}"
    st.rerun()

# ----------------------------
# 📊 Expense Trends + Charts
# ----------------------------
st.header("📊 Expense Trends")

with st.expander("Click to view Expense Trends"):
    try:
        res = requests.get(f"{BASE_URL}/expense/trends", params={"user_id": user_id}, timeout=10)
        if res.status_code == 200:
            data = res.json()
            st.subheader("📅 Daily Totals")
            if data.get("daily_totals"):
                st.bar_chart(pd.Series(data["daily_totals"]))
            else:
                st.info("No daily data yet.")

            st.subheader("📂 Spending by Category")
            if data.get("categories"):
                st.bar_chart(pd.Series(data["categories"]))
            else:
                st.info("No category data yet.")

            st.json(data)
        else:
            st.warning(f"Could not fetch trends: {res.status_code}")

    except Exception as e:
        st.warning(f"Could not load trends: {e}")

# ----------------------------
# 💡 Saving Tip
# ----------------------------
st.header("💡 Saving Tip")

if st.button("Get Tip"):
    try:
        res = requests.get(f"{BASE_URL}/expense/tip", params={"user_id": user_id}, timeout=10)
        if res.status_code == 200:
            data = res.json()
            st.info(data.get("tip", "No tip available."))
            if data.get("streak"):
                st.success(data["streak"])
        else:
            st.warning(f"Tip request failed: {res.status_code}")
    except Exception as e:
        st.warning(f"Could not fetch tip: {e}")

# ----------------------------
# 📅 Weekly Budget
# ----------------------------
st.header("💰 Weekly Budget Settings")

if st.session_state.budget_message:
    st.success(st.session_state.budget_message)
    st.session_state.budget_message = ""

if st.session_state.current_budget_message:
    st.info(st.session_state.current_budget_message)
    st.session_state.current_budget_message = ""

budget = st.number_input("Set new weekly budget", min_value=0.0)

if st.button("Update Budget"):
    try:
        res = requests.post(
            f"{BASE_URL}/budget",
            json={"weekly_budget": budget},
            params={"user_id": user_id},
            timeout=10
        )
        if res.status_code == 200:
            new_budget = res.json().get("weekly_budget", budget)
            st.session_state.budget_message = f"Budget updated: ₹{new_budget:.2f}"
        else:
            st.session_state.budget_message = f"Update failed: {res.status_code}"
    except Exception as e:
        st.session_state.budget_message = f"Request failed: {e}"
    st.rerun()

if st.button("Get Current Budget"):
    try:
        res = requests.get(f"{BASE_URL}/budget", params={"user_id": user_id}, timeout=10)
        if res.status_code == 200:
            current = res.json().get("weekly_budget", 0)
            st.session_state.current_budget_message = f"Weekly Budget: ₹{current:.2f}"
        else:
            st.session_state.current_budget_message = f"Failed: {res.status_code}"
    except Exception as e:
        st.session_state.current_budget_message = f"Could not fetch budget: {e}"
    st.rerun()

# ----------------------------
# 📤 Export Expenses
# ----------------------------
st.header("📤 Export Expenses")

if st.button("Export to CSV"):
    try:
        res = requests.get(f"{BASE_URL}/expenses/export", params={"user_id": user_id}, timeout=10)
        if res.status_code == 200:
            csv_data = res.text
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"expenses_{user_id}.csv",
                mime="text/csv"
            )
        else:
            st.warning(f"Export failed: {res.status_code}")
    except Exception as e:
        st.warning(f"Could not export: {e}")
