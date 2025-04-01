from xerberus import XerberusMetricsClient
import matplotlib.pyplot as plt

# ---------------------------------------------
# Initialize the client
# ---------------------------------------------
client = XerberusMetricsClient()

# ---------------------------------------------
# Define the date and chain to pull from
# ---------------------------------------------
target_date = "2025-03-01"
target_chain = "CARDANO"

# ---------------------------------------------
# Query metrics for top tokens by wallet count
# ---------------------------------------------
result = client.metrics_get(
    chains=[target_chain],
    partition_date=[target_date],
    sort_by="wallet_count",
    sort_order="DESC",
    limit=50
)

# ---------------------------------------------
# Extract relevant values for plotting
# ---------------------------------------------
x = []
y = []
labels = []

for m in result["metrics"]:
    dominance = m.get("dominance")
    wallet_count = m.get("wallet_count")
    symbol = m.get("token", {}).get("symbol", "N/A")

    if dominance is not None and wallet_count is not None:
        x.append(dominance)
        y.append(wallet_count)
        labels.append(symbol)

# ---------------------------------------------
# Create scatter plot
# ---------------------------------------------
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color="teal", alpha=0.7)

# Annotate points with token symbols
for i, label in enumerate(labels):
    plt.annotate(label, (x[i], y[i]), fontsize=8, alpha=0.7)

plt.title(f"Dominance vs Wallet Count on {target_date} ")
plt.xlabel("Dominance")
plt.ylabel("Wallet Count")
plt.grid(True)
plt.tight_layout()
plt.show()