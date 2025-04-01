import pytest
from xerberus import XerberusMetricsClient

client = XerberusMetricsClient()

LIST_SORT_ORDER = ["ASC", "DESC"]
LIST_SORT_BY_METRICS = ["", "", ""]
LIST_CHAINS = [None, "", ""]


def test_chains_get():
    chains = client.chains_get()
    assert isinstance(chains, list)
    assert "ETHEREUM" in chains
    print(chains)


def test_tokens_get_default():
    result = client.tokens_get()
    tokens = result["tokens"]
    assert isinstance(tokens, list)
    assert len(tokens) > 0
    assert all("symbol" in t and "address" in t and "chain" in t for t in tokens)


def test_tokens_get_uppercase_chain():
    result = client.tokens_get(chain="ETHEREUM")
    tokens = result["tokens"]
    assert isinstance(tokens, list)
    assert all(t["chain"].upper() == "ETHEREUM" for t in tokens)


def test_tokens_get_lowercase_chain():
    result = client.tokens_get(chain="polygon")
    tokens = result["tokens"]
    assert isinstance(tokens, list)
    assert all(t["chain"].upper() == "POLYGON" for t in tokens)


def test_tokens_pagination():
    page1 = client.tokens_get(limit=5, offset=0)["tokens"]
    page2 = client.tokens_get(limit=5, offset=5)["tokens"]
    assert isinstance(page1, list)
    assert isinstance(page2, list)
    assert page1 != page2  # Different slices


def test_tokens_sort_desc():
    result = client.tokens_get(sort_by="symbol", sort_order="DESC", limit=5)
    tokens = result["tokens"]
    symbols = [t["symbol"] for t in tokens]
    assert symbols == sorted(symbols, reverse=True)


def test_tokens_invalid_sort_field():
    with pytest.raises(Exception) as exc_info:
        client.tokens_get(sort_by="INVALID_FIELD")
    assert "Invalid sorting field" in str(exc_info.value)


def test_tokens_by_similar_symbol():
    result = client.tokens_by_similar_symbol("trump")
    tokens = result["tokens"]
    assert isinstance(tokens, list)
    assert result["total_count"] >= len(tokens)
    print(tokens)


def test_tokens_by_similar_address():
    result = client.tokens_by_similar_address(address="0x", limit=5)
    tokens = result["tokens"]
    assert isinstance(tokens, list)
    assert all("address" in t for t in tokens)
    print(tokens)


def test_metrics_get_minimal():
    result = client.metrics_get(partition_date="2025-01-01", limit=1)
    assert "metrics" in result
    assert "total_count" in result
    assert "current_count" in result
    assert isinstance(result["metrics"], list)


def test_metrics_get_with_chain():
    result = client.metrics_get(
        partition_date="2025-01-01", chains=["ETHEREUM"], limit=1
    )
    assert isinstance(result["metrics"], list)


def test_metrics_get_with_address():
    address = "0xfd9fa4f785331ce88b5af8994a047ba087c705d8"
    result = client.metrics_get(partition_date="2025-01-01", address=[address], limit=1)
    assert isinstance(result["metrics"], list)


def test_metrics_get_with_sorting():
    result = client.metrics_get(
        partition_date="2025-01-01",
        sort_by="wallet_count",
        sort_order="DESC",
        limit=1
    )
    assert isinstance(result["metrics"], list)


def test_metrics_get_combined_filters():
    result = client.metrics_get(
        partition_date="2025-01-01",
        address=["0xfd9fa4f785331ce88b5af8994a047ba087c705d8"],
        chains=["BASE_PROTOCOL"],
        sort_by="wallet_count",
        sort_order="DESC",
        limit=1,
    )
    assert isinstance(result["metrics"], list)