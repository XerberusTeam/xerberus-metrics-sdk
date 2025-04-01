from xerberus import XerberusMetricsClient
import matplotlib.pyplot as plt

client = XerberusMetricsClient()

# ---------------------------------------------
# Target token to track (by address and chain)
# ---------------------------------------------
token_address = "0xfd9fa4f785331ce88b5af8994a047ba087c705d8"
token_chain = "BASE_PROTOCOL"

# ---------------------------------------------
# Dates to compare (sorted oldest to newest)
# ---------------------------------------------
partition_dates = [
    "2025-01-01",
    "2025-01-08",
    "2025-01-15",
    "2025-01-22",
    "2025-01-29",
    "2025-02-05",
    "2025-02-12"
]

# ---------------------------------------------
# Fetch metrics for the given token and dates
# ---------------------------------------------
result = client.metrics_get(
    address=[token_address],
#    chains=[token_chain],
    partition_date=partition_dates,
    sort_by="partition_date",
    sort_order="ASC"
)

# ---------------------------------------------
# Prepare the data for plotting
# ---------------------------------------------
metrics = result["metrics"]
dates = [m["partition_date"] for m in metrics]
wallet_counts = [m["wallet_count"] for m in metrics]

# ---------------------------------------------
# Plot the time series
# ---------------------------------------------
plt.figure(figsize=(10, 5))
plt.plot(dates, wallet_counts, marker="o", linestyle="-", color="blue")

plt.title("Wallet Count Over Time")
plt.xlabel("Date")
plt.ylabel("Wallet Count")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()