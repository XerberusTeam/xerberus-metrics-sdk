
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
from collections import defaultdict
from xerberus import XerberusMetricsClient


# Initialize client
client = XerberusMetricsClient()

# 1. Define target date and lookback range
target_day = datetime.date(2025, 3, 1)
days_back = 30
date_list = [(target_day - datetime.timedelta(days=i)).isoformat() for i in range(days_back)]

# 2. Get top tokens by wallet_count on the target date
top_tokens_result = client.metrics_get(
    partition_date=[target_day.isoformat()],
    sort_by="wallet_count",
    sort_order="DESC",
    limit=30
)

top_assets = [
    {
        "asset_id": m["token"]["asset_id"],
        "chain": m["token"]["chain"],
        "symbol": m["token"]["symbol"]
    }
    for m in top_tokens_result["metrics"]
    if m.get("token") and m["token"].get("asset_id")
]

# 3. Fetch metrics one day at a time to reduce load
from time import sleep

addresses = [m["token"]["address"] for m in top_tokens_result["metrics"] if m.get("token")]
token_data = defaultdict(list)

for date in date_list:
    try:
        print(f"Fetching data for {date}...")
        metrics_result = client.metrics_get(
            address=addresses,
            partition_date=[date],
            limit=100  # adjust if needed per day
        )

        for m in metrics_result.get("metrics", []):
            token = m.get("token", {})
            symbol = token.get("symbol", "UNKNOWN")
            token_data[symbol].append({
                "date": m["partition_date"],
                "wallet_count": m.get("wallet_count"),
                "dominance": m.get("dominance")
            })

        # Optional: small delay between requests to avoid hammering the server
        sleep(0.2)

    except Exception as e:
        print(f"⚠️ Error on {date}: {e}")


# 5. Plot evolution
# Extract all dates in sorted order
all_dates = sorted({e["date"] for entries in token_data.values() for e in entries})
fig, ax = plt.subplots(figsize=(12, 8))

# Use a consistent color per token
cmap = plt.get_cmap("tab20")
token_colors = {
    symbol: cmap(i % 20)
    for i, symbol in enumerate(sorted(token_data.keys()))
}

def update(frame):
    ax.clear()
    current_date = all_dates[frame]
    ax.set_title(f"Dominance vs Wallet Count — {current_date}", fontsize=16)

    for symbol, entries in token_data.items():
        point = next((e for e in entries if e["date"] == current_date), None)
        if point and point["dominance"] is not None and point["wallet_count"] is not None:
            ax.scatter(
                point["dominance"],
                point["wallet_count"],
                label=symbol,
                color=token_colors[symbol],
                s=40,
                alpha=0.8
            )

    ax.set_xlabel("Dominance")
    ax.set_ylabel("Wallet Count")
    ax.grid(True)
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    ax.set_xlim(0, 1)  # Adjust based on expected dominance range
    ax.set_ylim(0, max(e["wallet_count"] for entries in token_data.values() for e in entries if e["wallet_count"]))

# Create animation
anim = animation.FuncAnimation(
    fig,
    update,
    frames=len(all_dates),
    interval=600,
    repeat=False
)

# Save to gif
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "dominance_vs_wallets.gif")
anim.save(save_path, writer="pillow", fps=3)
print(" GIF saved as 'dominance_vs_wallets.gif'")