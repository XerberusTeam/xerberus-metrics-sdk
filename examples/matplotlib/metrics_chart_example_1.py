from xerberus import XerberusMetricsClient
import matplotlib.pyplot as plt


client = XerberusMetricsClient()

# ---------------------------------------------
# Query top tokens by wallet count for a specific day
# ---------------------------------------------
result = client.metrics_get(
    partition_date=["2025-03-01"],
    sort_by="wallet_count",
    sort_order="DESC",
    limit=10  # Show top 10 tokens
)

metrics = result["metrics"]

# ---------------------------------------------
# Extract symbols and wallet counts for plotting
# ---------------------------------------------
symbols = [metric["token"]["symbol"] for metric in metrics]
wallet_counts = [metric["wallet_count"] for metric in metrics]

# ---------------------------------------------
# Plot the results using matplotlib
# ---------------------------------------------
plt.figure(figsize=(10, 6))
bars = plt.bar(symbols, wallet_counts)

plt.title("Top Tokens by Wallet Count on 2025-03-01")
plt.xlabel("Token Symbol")
plt.ylabel("Wallet Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Show the values on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, f"{int(yval)}", ha='center', va='bottom')

plt.show()