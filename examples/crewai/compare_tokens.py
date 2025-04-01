from datetime import date, timedelta
from crewai import Agent, Task, Crew
from xerberus import XerberusMetricsClient

# 1. Load SDK client
sdk = XerberusMetricsClient()

# 2. Tool function to get token metrics
def get_token_metrics(symbol: str) -> dict:
    """Fetch token metrics over the last 30 days for a given symbol"""
    end_date = date.today()
    date_list = [(end_date - timedelta(days=i)).isoformat() for i in range(30)]

    result = sdk.tokens_by_similar_symbol(symbol)
    if not result["tokens"]:
        return {"error": f"No data found for {symbol}"}

    token_address = result["tokens"][0]["address"]
    token_chain = result["tokens"][0]["chain"]

    metrics = sdk.metrics_get(
        address=[token_address],
        chains=[token_chain],
        partition_date=date_list
    )

    return {
        "symbol": symbol.upper(),
        "metrics": metrics["metrics"]
    }

# 3. Define the CrewAI agent (no LangChain)
analyst = Agent(
    role="Crypto Market Analyst",
    goal="Compare two crypto tokens based on dominance, wallet count, and growth",
    backstory="An expert at analyzing token momentum and wallet behavior over time.",
    allow_delegation=False,
    verbose=True
)

# 4. Define the comparison task
def build_comparison_task(symbol1, symbol2):
    token1 = get_token_metrics(symbol1)
    token2 = get_token_metrics(symbol2)

    return Task(
        description=(
            f"Compare the following token data:\n\n"
            f"Token 1: {token1}\n\n"
            f"Token 2: {token2}\n\n"
            f"Evaluate metrics such as dominance, wallet count, price changes, and lifecycle metrics. "
            f"Decide which token is stronger and provide a short markdown-formatted summary."
        ),
        agent=analyst,
        expected_output="A markdown summary of which token is better with evidence."
    )

# 5. Crew Orchestration
def compare_tokens(symbol1, symbol2):
    task = build_comparison_task(symbol1, symbol2)

    crew = Crew(
        agents=[analyst],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    print("\n Token Comparison Result:\n")
    print(result)

# Run directly
if __name__ == "__main__":
    compare_tokens("SNEK", "COCK")
