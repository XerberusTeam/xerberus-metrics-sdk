# bullish_bearish_crew.py
from crewai import Agent, Crew, Task
from xerberus import XerberusMetricsClient
from datetime import datetime, timedelta

# Initialize Xerberus client
client = XerberusMetricsClient()

# ----------------------------------------
# Helper: Check if a metric is increasing
# ----------------------------------------
def metrics_is_increasing(metrics, field):
    values = [m[field] for m in sorted(metrics, key=lambda x: x["partition_date"]) if m.get(field) is not None]
    return values[-1] > values[0] if len(values) >= 2 else False

# ----------------------------------------
# Agent 1: Data fetcher
# ----------------------------------------
data_fetcher = Agent(
    name="DataFetcherAgent",
    role="Token Metrics Retriever",
    goal="Fetch 7-day metrics for a given token address",
    backstory="You interface with the Xerberus GraphQL API to retrieve on-chain token metrics.",
    verbose=True,
)

def fetch_metrics_task(token_address):
    today = datetime.utcnow().date()
    date_range = [(today - timedelta(days=i)).isoformat() for i in range(8)]  # 0 to 7

    def execute():
        return client.metrics_get(
            address=[token_address],
            partition_date=date_range,
            limit=100
        )

    return Task(
        description=f"Fetch 7-day metrics for token {token_address}",
        expected_output="Dictionary of daily metrics",
        agent=data_fetcher,
        async_execution=False,
        output_key="metrics",
        func=execute
    )

# ----------------------------------------
# Agent 2: Trend analyzer
# ----------------------------------------
trend_analyzer = Agent(
    name="TrendAnalyzerAgent",
    role="Trend Analyzer",
    goal="Analyze trend of wallet count, price and dominance for a token",
    backstory="You analyze 7-day trends to help classify token behavior.",
    verbose=True,
)

trend_analysis_task = Task(
    description="Analyze whether the metrics show bullish behavior.",
    expected_output="JSON with fields like wallet_growth, price_growth, dominance_growth",
    agent=trend_analyzer,
    async_execution=False,
    input_keys=["metrics"],
    output_key="trend_summary",
    func=lambda inputs: {
        "wallet_growth": metrics_is_increasing(inputs["metrics"], "wallet_count"),
        "price_growth": metrics_is_increasing(inputs["metrics"], "typical_price"),
        "dominance_growth": metrics_is_increasing(inputs["metrics"], "dominance"),
    }
)

# ----------------------------------------
# Agent 3: Classifier
# ----------------------------------------
classifier = Agent(
    name="ClassifierAgent",
    role="Bullishness Classifier",
    goal="Classify a token as bullish or bearish",
    backstory="Based on the trend analysis, decide whether the token is bullish or bearish.",
    verbose=True,
)

classification_task = Task(
    description="Make final classification of bullish or bearish",
    expected_output="String: either 'Bullish' or 'Bearish'",
    agent=classifier,
    input_keys=["trend_summary"],
    func=lambda inputs: "Bullish" if sum(inputs["trend_summary"].values()) >= 2 else "Bearish"
)

# ----------------------------------------
# Crew Execution
# ----------------------------------------
if __name__ == "__main__":
    token_address = "0xfd9fa4f785331ce88b5af8994a047ba087c705d8"  # Example

    crew = Crew(
        agents=[data_fetcher, trend_analyzer, classifier],
        tasks=[
            fetch_metrics_task(token_address),
            trend_analysis_task,
            classification_task
        ],
        verbose=True
    )

    result = crew.kickoff()
    print("\nFinal Classification:", result)
