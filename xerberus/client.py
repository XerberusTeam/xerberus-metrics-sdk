import os
import requests
from .config import get_config

def load_query(name):
    with open(os.path.join(os.path.dirname(__file__), "queries", f"{name}.graphql"), "r") as f:
        return f.read()


class XerberusMetricsClient:
    def __init__(self, api_url=None, api_key=None):
        config = get_config()
        self.api_url = api_url or config["API_URL"]
        self.api_key = api_key or config["API_KEY"]

        if not self.api_key:
            raise ValueError("Missing API key. Please provide it via constructor or set API_KEY in your environment.")

        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

    def metrics_get(
        self,
        partition_date,
        address=None,
        chains=None,
        limit=10,
        offset=0,
        sort_by="partition_date",
        sort_order="ASC"
    ):
        """
        Fetches token metrics from the API with optional filtering and sorting.
        """
        query = load_query("metrics")

        if not isinstance(partition_date, list):
            partition_date = [partition_date]
        if address and not isinstance(address, list):
            address = [address]
        if chains and not isinstance(chains, list):
            chains = [chains]

        variables = {
            "partition_date": partition_date,
            "address": address or [],
            "chains": chains or [],
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by,
            "sortOrder": sort_order
        }

        response = self._execute(query, variables)
        return {
            "metrics": response["metrics"]["metrics"],
            "total_count": response["metrics"]["total_count"],
            "current_count": response["metrics"]["current_count"],
        }

    def tokens_get(self, chain=None, limit=10, offset=0, sort_by="symbol", sort_order="ASC"):
        with open("xerberus/queries/tokens.graphql") as f:
            query = f.read()

        variables = {
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by.upper(),
            "sortOrder": sort_order.upper(),
        }

        if chain:
            if isinstance(chain, str):
                variables["chain"] = [chain.upper()]
            elif isinstance(chain, list):
                variables["chain"] = [c.upper() for c in chain]
            else:
                raise ValueError("`chain` must be a string or list of strings")

        response = self._execute(query, variables)
        tokens_data = response.get("tokens", {})

        return {
            "tokens": tokens_data.get("tokens", []),
            "total_count": tokens_data.get("total_count", 0),
        }

    def chains_get(self):
        " Retrieves a list of all supported chains."
        query = load_query("chains")
        return self._execute(query, {})["chains"]

    def tokens_by_similar_symbol(self, symbol, limit=10, offset=0, sort_by="symbol", sort_order="ASC"):
        """
        Returns tokens where the symbol contains the given substring.
        """
        query = load_query("tokens_by_similar_symbol")
        variables = {
            "symbol": symbol,
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by.upper(),
            "sortOrder": sort_order.upper()
        }
        response = self._execute(query, variables)

        return {
            "tokens": response["tokensBySimilarSymbol"]["tokens"],
            "total_count": response["tokensBySimilarSymbol"]["total_count"]
        }



    def tokens_by_similar_address(self, address, limit=10, offset=0, sort_by="symbol", sort_order="ASC"):
        """Search tokens by a substring match on address."""
        query = load_query("tokens_by_similar_address")
        variables = {
            "address": address,
            "limit": limit,
            "offset": offset,
            "sortBy": sort_by.upper(),
            "sortOrder": sort_order.upper()
        }
        response = self._execute(query, variables)

        return {
            "tokens": response["tokensBySimilarAddress"]["tokens"],
            "total_count": response["tokensBySimilarAddress"]["total_count"]
        }


    def _execute(self, query, variables):
        payload = {
            "query": query,
            "variables": variables,
        }
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            try:
                error_data = response.json()
                print("[ERROR] GraphQL Error Response:", error_data)
                if "errors" in error_data:
                    messages = "; ".join(error["message"] for error in error_data["errors"])
                    raise Exception(f"GraphQL Error: {messages}")
            except Exception:
                raise http_err

        data = response.json()
        
        if "errors" in data:
            messages = "; ".join(error["message"] for error in data["errors"])
            raise Exception(f"GraphQL Error: {messages}")
        
        if "data" not in data:
            raise Exception(f"Missing 'data' in response: {data}")

        return data.get("data")
