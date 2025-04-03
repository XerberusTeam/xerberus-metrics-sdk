from dotenv import load_dotenv
import os
from xerberus import XerberusMetricsClient

load_dotenv()
# Initialize the client (optionally pass api_url if testing locally)
client = XerberusMetricsClient(api_key=os.getenv("XERBERUS_API_KEY"),api_email=os.getenv("XERBERUS_API_EMAIL"))

# -------------------------------
# Example 1: Search tokens by similar symbol
# -------------------------------
print(" Example: Search tokens by symbol substring (e.g., 'trump')")

symbol_search = client.tokens_by_similar_symbol("trump", limit=5)

print("Total tokens found:", symbol_search["total_count"])
for token in symbol_search["tokens"]:
    print(f"{token['symbol']} - {token['address']} ({token['chain']})")

# -------------------------------
# Example 2: Search tokens by address substring
# -------------------------------
print("\n Example: Search tokens by partial address (e.g., '0x')")

address_search = client.tokens_by_similar_address(address="0x", limit=5)

print("Total tokens found:", address_search["total_count"])
for token in address_search["tokens"]:
    print(f"{token['symbol']} - {token['address']} ({token['chain']})")

