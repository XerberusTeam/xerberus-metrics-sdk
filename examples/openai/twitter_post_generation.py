import os
from dotenv import load_dotenv
from openai import OpenAI
from xerberus import XerberusMetricsClient

# Load environment variables from a .env file (e.g., OPENAI_API_KEY)
load_dotenv()

# Initialize the Xerberus GraphQL client
client = XerberusMetricsClient()

# Initialize OpenAI client using API key from environment
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Fetch top 3 tokens with the highest 1-day wallet growth for a specific date
result = client.metrics_get(
    partition_date=["2025-03-11"],
    sort_by="wallet_count_change_1D",
    sort_order="DESC",
    limit=3
)

# 2. Format data as numbered list for the prompt context
context_lines = []
context_lines.append("wallet_count_change_1D")
for i, metric in enumerate(result["metrics"]):
    token = metric.get("token", {})
    symbol = token.get("symbol", "UNKNOWN")
    change = metric.get("wallet_count_change_1D", "N/A")
    context_lines.append(f"{i+1}. ${symbol} - {change:+.1f} count")

context = "\n".join(context_lines)

# 3. Generate tweet using OpenAI (GPT-4-turbo) in a research-style tone with only 1 emoji
response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a social media strategist for a crypto analytics platform."},
        {"role": "user", "content": f"Write a tweet summarizing this crypto data:\n{context}\nKeep it under 280 characters and include no emoji."}
    ]
)

# 4. Extract and print the generated tweet
tweet_text = response.choices[0].message.content
print("Generated Tweet:\n", tweet_text)
