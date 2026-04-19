import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/expenses.csv")

# -----------------------------
# 🧹 DATA CLEANING
# -----------------------------
df = df.drop_duplicates()
df = df.dropna(subset=['Date', 'Category', 'Amount', 'Type'])

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

df['Category'] = df['Category'].str.strip().str.title()
df['Type'] = df['Type'].str.strip().str.title()

# -----------------------------
# 🧠 FEATURE ENGINEERING
# -----------------------------
df['Month'] = df['Date'].dt.month_name()
df['Month_Num'] = df['Date'].dt.month
df['Weekday'] = df['Date'].dt.day_name()

# Save cleaned data
df.to_csv("data/cleaned_expenses.csv", index=False)

print("✅ Data cleaned and saved!")

# -----------------------------
# 📊 VISUALIZATION
# -----------------------------
sns.set(style="whitegrid")

# Category Spending
category_sum = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
sns.barplot(x=category_sum.index, y=category_sum.values)
plt.xticks(rotation=45)
plt.title("Category-wise Spending")
plt.tight_layout()
plt.savefig("outputs/category_spending.png")
plt.show()

# Pie Chart
expense_df = df[df['Type'] == 'Expense']
category_expense = expense_df.groupby('Category')['Amount'].sum()

plt.figure(figsize=(6,6))
plt.pie(category_expense, labels=category_expense.index, autopct='%1.1f%%')
plt.title("Expense Distribution")
plt.savefig("outputs/pie_chart.png")
plt.show()

# Monthly Trend
monthly_expense = df[df['Type'] == 'Expense'].groupby('Month_Num')['Amount'].sum()
monthly_income = df[df['Type'] == 'Income'].groupby('Month_Num')['Amount'].sum()

plt.figure(figsize=(10,5))
monthly_expense.plot(marker='o', label='Expense')
monthly_income.plot(marker='o', label='Income')
plt.legend()
plt.title("Monthly Trend")
plt.savefig("outputs/monthly_trend.png")
plt.show()

# -----------------------------
# 🧠 INSIGHTS
# -----------------------------
print("\n🧠 Insights:")
print("Top Category:", category_sum.idxmax())

if monthly_expense.sum() > monthly_income.sum():
    print("⚠️ Overspending detected")
else:
    print("✅ Good savings habit")