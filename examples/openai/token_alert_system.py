import os
from dotenv import load_dotenv
from xerberus import XerberusMetricsClient
from openai import OpenAI
from datetime import datetime
import html

# Load environment variables (like your OPENAI_API_KEY) from a .env file
load_dotenv()

# Initialize Xerberus client (for GraphQL metrics)
client = XerberusMetricsClient()

# Initialize OpenAI client using the API key from environment
openai = OpenAI()


# 1. Detect alerts based on some heuristic (e.g., wallet_count_change_7D > 20)
def detect_alerts(metrics):
    alerts = []
    for metric in metrics:
        if metric.get("wallet_count_change_7D", 0) > 20:
            alerts.append(
                {
                    "token": metric["token"],
                    "wallet_change": metric["wallet_count_change_7D"],
                    "dominance": metric.get("dominance"),
                    "reason": "High 7-day wallet growth",
                }
            )
    return alerts


# 2. Use OpenAI to generate a readable summary — returned as HTML
def generate_summary(alerts):
    prompt = "You are a crypto analyst. Write a short, research-style HTML summary of the following flagged crypto tokens and explain why they might be bullish:\n\n"
    for alert in alerts:
        token = alert["token"]
        prompt += f"- {token['symbol']} ({token['chain']}) — {alert['reason']} (Wallet change: {alert['wallet_change']}, Dominance: {alert['dominance']})\n"

    response = openai.chat.completions.create(
        model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}]
    )

    # Return formatted HTML summary
    summary = response.choices[0].message.content
    summary_html = summary.replace("\n", "<br>")
    return f"<div>{summary_html}</div>"


# 3. Generate a full HTML report
def generate_html_report(summary, alerts):
    today = datetime.now().strftime("%Y-%m-%d")

    # Table rows for flagged tokens
    rows = "".join(
        f"<tr><td>{html.escape(a['token']['symbol'])}</td><td>{a['wallet_change']}</td><td>{a['reason']}</td></tr>"
        for a in alerts
    )

    return f"""
    <html>
    <head>
        <title>Token Alert Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 2em; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
        </style>
    </head>
    <body>
        <h1>Token Alert Report </h1>
        <h2>Flagged Tokens</h2>
        <table>
            <tr><th>Token</th><th>7D Wallet Change</th><th>Reason</th></tr>
            {rows}
        </table>
        {summary}
    </body>
    </html>
    """


# 4. Main flow: fetch metrics, detect alerts, generate summary, save HTML
metrics = client.metrics_get(partition_date=["2025-03-10"], limit=100)["metrics"]
alerts = detect_alerts(metrics)

if alerts:
    summary = generate_summary(alerts)
    report = generate_html_report(summary, alerts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_dir, "alert_report.html")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(report)
    print("Report saved: alert_report.html")
else:
    print("No significant token behavior detected.")
