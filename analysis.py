import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "supermarket_sales.csv", parse_dates=["Date"])

print("Dataset shape:", df.shape)
print("\nMissing values:\n", df.isna().sum())
print("\nSummary:\n", df[["Quantity", "Unit_Price", "Sales", "COGS", "Profit", "Rating"]].describe())

monthly = df.groupby(df["Date"].dt.to_period("M")).agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum")
).reset_index()
monthly["Date"] = monthly["Date"].astype(str)

category = df.groupby("Category").agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum")
).sort_values("Sales", ascending=False)

branch = df.groupby(["Branch", "City"]).agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum"), Transactions=("Invoice_ID", "count")
).reset_index().sort_values("Sales", ascending=False)

payment = df.groupby("Payment_Method").agg(
    Sales=("Sales", "sum"), Transactions=("Invoice_ID", "count")
).sort_values("Sales", ascending=False)

customer = df.groupby("Customer_Type").agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum"), Transactions=("Invoice_ID", "count")
)

print("\nTop categories:\n", category)
print("\nBranch performance:\n", branch)
print("\nPayment methods:\n", payment)
print("\nCustomer types:\n", customer)

print("\nKey business insights:")
print(f"- Total sales: ₹{df['Sales'].sum():,.2f}")
print(f"- Total profit: ₹{df['Profit'].sum():,.2f}")
print(f"- Overall profit margin: {(df['Profit'].sum()/df['Sales'].sum())*100:.2f}%")
print(f"- Best-selling category: {category.index[0]}")
print(f"- Highest-sales branch: {branch.iloc[0]['Branch']} ({branch.iloc[0]['City']})")
print(f"- Most-used payment method: {payment.index[0]}")

out = BASE / "visualizations"
out.mkdir(exist_ok=True)

plt.figure(figsize=(9,5))
plt.plot(monthly["Date"], monthly["Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(out/"monthly_sales.png", dpi=160)
plt.close()

plt.figure(figsize=(9,5))
plt.bar(category.index, category["Sales"])
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales (₹)")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(out/"category_sales.png", dpi=160)
plt.close()

plt.figure(figsize=(7,5))
plt.bar(branch["Branch"], branch["Sales"])
plt.title("Sales by Branch")
plt.xlabel("Branch")
plt.ylabel("Sales (₹)")
plt.tight_layout()
plt.savefig(out/"branch_sales.png", dpi=160)
plt.close()

plt.figure(figsize=(8,5))
plt.bar(payment.index, payment["Transactions"])
plt.title("Transactions by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(out/"payment_transactions.png", dpi=160)
plt.close()

print("\nCharts saved in visualizations/")
