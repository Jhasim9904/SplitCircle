from fastapi import FastAPI, Response
from pydantic import BaseModel
from collections import defaultdict
from fastmcp import FastMCP, ModelNode
import json
import csv
from io import StringIO

# ------------------------
# 📂 Local JSON storage
# ------------------------
class ExpenseStorage:
    def __init__(self, storage_file="expenses.json"):
        self.file = storage_file
        self._load()

    def _load(self):
        try:
            with open(self.file) as f:
                self.data = json.load(f)
                if not isinstance(self.data, dict):
                    raise ValueError("Storage must be a JSON object.")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.data = {"expenses": [], "weekly_budget": 200.0}
            self._save()

    def _save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)

    def log_expense(self, expense):
        self.data["expenses"].append(expense)
        self._save()

    def get_expenses(self):
        return self.data["expenses"]

    def set_budget(self, amount):
        self.data["weekly_budget"] = amount
        self._save()

    def get_budget(self):
        return self.data.get("weekly_budget", 200.0)

# ------------------------
# 🤖 Agents with Smart Categorization
# ------------------------
class ExpenseLoggerAgent(ModelNode):
    def __init__(self, storage):
        super().__init__(name="ExpenseLoggerAgent")
        self.storage = storage

        self.category_map = {
            "juice": "Food",
            "coffee": "Food",
            "snack": "Food",
            "restaurant": "Food",
            "canteen": "Food",
            "mess ": "Food",
            "lunch": "Food",
            "taxi": "Transport",
            "uber": "Transport",
            "rapido": "Transport",
            "ola": "Transport",
            "bus": "Transport",
            "petrol": "Transport",
            "fuel": "Transport",
            "movie": "Entertainment",
            "subscription": "Entertainment",
            "rent": "Housing",
            "grocery": "Groceries",
        }

    def smart_categorize(self, category_text, note_text):
        combined = f"{category_text} {note_text}".lower()
        for keyword, mapped in self.category_map.items():
            if keyword in combined:
                return mapped
        return category_text if category_text.strip() else "Misc"

    def run(self, **kwargs):
        expense = kwargs["expense"]
        original = expense.get("category", "")
        note = expense.get("note", "")
        expense["category"] = self.smart_categorize(original, note)
        self.storage.log_expense(expense)
        return {
            "status": f"✅ Expense logged! (Category: {expense['category']})",
            "expense": expense
        }

class BudgetTrendAgent(ModelNode):
    def __init__(self, storage):
        super().__init__(name="BudgetTrendAgent")
        self.storage = storage

    def run(self, **kwargs):
        expenses = self.storage.get_expenses()
        daily = defaultdict(float)
        categories = defaultdict(float)

        for exp in expenses:
            daily[exp["date"]] += exp["amount"]
            categories[exp["category"]] += exp["amount"]

        return {
            "daily_totals": dict(daily),
            "weekly_total": sum(daily.values()),
            "weekly_budget": self.storage.get_budget(),
            "categories": dict(categories)
        }

class SavingTipAgent(ModelNode):
    def __init__(self, storage):
        super().__init__(name="SavingTipAgent")
        self.storage = storage

    def run(self, **kwargs):
        trends = BudgetTrendAgent(self.storage).run()
        spent = trends["weekly_total"]
        budget = trends["weekly_budget"]

        if spent > budget:
            tip = "⚠️ You’re over budget! Try cutting spending in your top category."
        elif spent > budget * 0.8:
            tip = "🟡 You’re close to hitting your weekly budget. Watch out!"
        else:
            tip = "✅ Nice! You're under budget this week."

        streak = "🔥 Good job! You stayed under budget." if spent <= budget else "Try again next week!"
        return {"tip": tip, "streak": streak}

# ------------------------
# 🧩 MCP Orchestrator
# ------------------------
storage = ExpenseStorage()
logger_agent = ExpenseLoggerAgent(storage)
trend_agent = BudgetTrendAgent(storage)
tip_agent = SavingTipAgent(storage)

mcp = FastMCP()
mcp.register_model(logger_agent)
mcp.register_model(trend_agent)
mcp.register_model(tip_agent)

# ------------------------
# 🚀 FastAPI app
# ------------------------
app = FastAPI(title="💸 Expense & Budget Buddy")

class Expense(BaseModel):
    date: str
    amount: float
    category: str | None = ""
    note: str | None = ""

class Budget(BaseModel):
    weekly_budget: float

@app.post("/expense")
def log_expense(expense: Expense):
    return mcp.run_model("ExpenseLoggerAgent", expense=expense.dict())

@app.get("/expense/trends")
def get_trends():
    return mcp.run_model("BudgetTrendAgent")

@app.get("/expense/tip")
def get_tip():
    return mcp.run_model("SavingTipAgent")

@app.post("/budget")
def set_budget(budget: Budget):
    storage.set_budget(budget.weekly_budget)
    return {"weekly_budget": storage.get_budget()}

@app.get("/budget")
def get_budget():
    return {"weekly_budget": storage.get_budget()}

@app.get("/expenses/export")
def export_expenses():
    expenses = storage.get_expenses()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["date", "amount", "category", "note"])
    writer.writeheader()
    writer.writerows(expenses)
    output.seek(0)
    return Response(content=output.read(), media_type="text/csv")

@app.post("/expenses/reset")
def reset_expenses():
    storage.data["expenses"] = []
    storage._save()
    return {"status": "✅ All expenses cleared!"}