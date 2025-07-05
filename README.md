# 💸 Expense & Budget Buddy — FastAPI + FastMCP

Smart Expense Buddy and Budget Tracker— Powered by FastAPI &amp; FastMCP for Agent-based Budget Management.

**Expense Buddy** is a practical **Model-Context-Protocol (MCP)** project that helps users **log expenses**, **manage budgets**, **visualize trends**, and **export expense logs as CSV**, all powered by **FastAPI**, **FastMCP**, and **Streamlit**, deployed fully serverless on **Render**.

---

## 🚀 **What It Solves**

Keeping track of everyday expenses manually is tedious — especially when you’re trying to stick to a weekly budget.  
**Expense Buddy** lets you:

- Log expenses with notes.
- Instantly see where your money goes with **weekly summaries**, top categories, and spending trends.
- Export all your logged expenses as a **CSV file** for easy backup or further analysis.
- **Reset** all data to start fresh anytime.
- Use **NLP-powered auto-categorization** — e.g., type "Rapido" and it’s smartly categorized as _Transportation_ which has been manually done for several most used keywords in our code.

This shows how an MCP pattern works in real life: the backend handles data processing, categorization, and storage, while the frontend focuses on user experience, visualization, and export.

---

## ⚙️ **Tech Stack**

- 🐍 **Python 3.11+**
- ⚡ **FastAPI** — lightweight backend API server.
- 🔗 **FastMCP** — Model Context Protocol for modular data flow.
- 🧠 **Custom NLP logic** — for auto-categorizing expenses.
- 🎨 **Streamlit** — simple and interactive web frontend.
- ☁️ **Render** — serverless deployment for backend & frontend.
- 📂 **JSON file storage** — keeps the project light without a database.

---

## 🗂️ **Project Structure**

Expense-Buddy/
├── backend/
│ ├── server.py # FastAPI server with FastMCP
│ ├── fastmcp.py # MCP node for NLP & processing
│ ├── expenses.json # Stores expenses & budget data
│ ├── requirements.txt
├── frontend/
│ ├── expense_client.py # Streamlit frontend app
│ ├── requirements.txt
├── README.md

---

## 🧩 **How It Works**

### ✅ **Backend (FastAPI + FastMCP)**

- Exposes endpoints like `/expense` and `/budget`.
- Uses **FastMCP** to modularize tasks like NLP category assignment.
- Stores data in a simple `expenses.json` file.

### ✅ **Frontend (Streamlit)**

- Lets users:
  - Set weekly budgets.
  - Log new expenses.
  - View weekly expense breakdowns & category trends.
  - **Export expense logs as a CSV** with one click.
  - Use the **sidebar** to check budget status and reset all data if needed.
- Connects to your FastAPI server deployed on **Render**.

### ✅ **NLP & Auto Categorization**

- Example: enter “Rapido” → it’s recognized as _Transportation_ using simple NLP matching.
- These mappings can be easily expanded to handle real-world use cases.

---

## 🌐 **Live Demo**

| Component           | URL                                                                                            |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| 🎨 **Frontend App** | [https://expense-buddy-frontend.onrender.com](https://expense-buddy-frontend.onrender.com)     |
| 🚀 **Backend API**  | [https://expense-buddy-mcp-server.onrender.com](https://expense-buddy-mcp-server.onrender.com) |

---

## 📈 **Real-World Use Case**

- 📊 **Budget Control**: Perfect for students, freelancers, or anyone needing a simple weekly budget tracker.
- 🧠 **NLP Smartness**: Shows how to add intelligence to expense logging with minimal code.
- 📤 **CSV Export**: Download your expenses anytime for backup or further analysis.
- ⚡ **MCP Architecture**: Demonstrates modular component processing in a clear way.
- ☁️ **Full Serverless**: Fully deployed on Render — accessible anywhere with a single link.

---

## ⚡ **How to Try It**

1. Open the **frontend app** → [Expense Buddy UI](https://expense-buddy-frontend.onrender.com)
2. Set your budget, log expenses, and see your weekly overview.
3. Click **Export CSV** to download your expense log.
4. Reset your data anytime with the sidebar reset button.
5. All actions talk directly to the **FastAPI server** → [Backend Server](https://expense-buddy-mcp-server.onrender.com)

---

## ✅ **Note on Data Persistence**

This project uses a simple **shared JSON file** for demonstration — this keeps the MCP concept clear and easy to understand.  
For production, each user’s data would be stored separately in a proper database (e.g., SQLite, Firebase) to avoid shared data and provide user isolation.

---

## 🏆 **Submission Checklist**

| Deliverable        | Link                                                                                                               |
| ------------------ | ------------------------------------------------------------------------------------------------------------------ |
| 📂 **GitHub Repo** | [https://github.com/Jhasim9904/Expense-Buddy-MCP-FastAPI](https://github.com/Jhasim9904/Expense-Buddy-MCP-FastAPI) |
| ⚙️ **Backend**     | [https://expense-buddy-mcp-server.onrender.com](https://expense-buddy-mcp-server.onrender.com)                     |
| 🎨 **Frontend**    | [https://expense-buddy-frontend.onrender.com](https://expense-buddy-frontend.onrender.com)                         |

---

## 🙌 **Author**

Built with passion by **Jhasim Hassan**

---

## 📜 **License**

For educational and demonstration purposes only.
