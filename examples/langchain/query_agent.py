# langchain_query_agent.py

from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import StructuredTool
from xerberus import XerberusMetricsClient

# Initialize your Xerberus SDK client
client = XerberusMetricsClient()

# Define tools (wrap SDK calls)
def top_tokens_by_wallet_count(chain: str = "ethereum", date: str = "2025-01-01", limit: int = 5):
    result = client.metrics_get(
        partition_date=[date],
        chains=chain,
        sort_by="wallet_count",
        sort_order="DESC",
        limit=limit
    )
    tokens = [f"{m['token']['symbol']} ({m['wallet_count']} wallets)" for m in result['metrics'] if m.get("token")]
    return f"Top {len(tokens)} tokens by wallet count on {chain} ({date}):\n" + "\n".join(tokens)

def top_token_by_dominance(date: str = "2025-01-01"):
    result = client.metrics_get(
        partition_date=[date],
        sort_by="dominance",
        sort_order="DESC",
        limit=1
    )
    metric = result['metrics'][0] if result['metrics'] else {}
    token = metric.get("token", {})
    return f"Top token by dominance on {date}: {token.get('symbol')} ({metric.get('dominance')}%)"

# Wrap the SDK methods as LangChain tools
tools = [
    StructuredTool.from_function(
        func=top_tokens_by_wallet_count,
        name="TopTokensByWalletCount",
        description="Gets the top N tokens by wallet count for a specific chain and date."
    ),
    StructuredTool.from_function(
        func=top_token_by_dominance,
        name="TopTokenByDominance",
        description="Returns the token with the highest dominance for a specific date."
    )
]

# Initialize LangChain agent
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# Example usage
if __name__ == "__main__":
    print(agent.run("What were the top 5 tokens by wallet count on Ethereum on 2025-01-01?"))
    print(agent.run("Which token had the highest dominance on January 1st, 2025?"))
