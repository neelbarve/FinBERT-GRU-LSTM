from unittest.mock import patch, MagicMock
from data_ingest.fetchers import fetch_news_newsapi_top, fetch_news_finnhub


@patch("data_ingest.fetchers.requests.get")
def test_fetch_news_newsapi_top_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"articles": [{"title": "Test Article"}]}
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    result = fetch_news_newsapi_top("fake_key", "market")
    assert result == [{"title": "Test Article"}]


@patch("data_ingest.fetchers.requests.get")
def test_fetch_news_newsapi_top_failure_returns_empty_list(mock_get):
    mock_get.side_effect = Exception("network error")

    result = fetch_news_newsapi_top("fake_key", "market")
    assert result == []


@patch("data_ingest.fetchers.requests.get")
def test_fetch_news_finnhub_success(mock_get):
    import datetime
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"headline": "Test"}]
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    from_dt = datetime.datetime(2026, 1, 1)
    to_dt = datetime.datetime(2026, 1, 2)
    result = fetch_news_finnhub("fake_key", "AAPL", from_dt, to_dt)
    assert result == [{"headline": "Test"}]
