from xerberus import XerberusMetricsClient

# Initialize the client (optionally pass api_url if testing locally)
client = XerberusMetricsClient()

# ---------------------------------------------
# Example: Fetch metrics for a specific date
# ---------------------------------------------
# In this example, we sort tokens by wallet count in descending order
# You can also filter by `chain`, `address`, and paginate with `limit` and `offset`
result = client.metrics_get(
    partition_date=["2025-03-01"],        # Required: One or more partition dates
    sort_by="wallet_count",               # Optional: Sort by any supported metric field
    sort_order="DESC",                    # Optional: 'ASC' or 'DESC' (default is 'ASC')
)

# ---------------------------------------------
# Print out the total and current counts
# ---------------------------------------------
print("Total Metrics:", result["total_count"])       # Total entries matching the filters
print("Current Page Count:", result["current_count"]) # Number of metrics returned in this request
print()
