from unittest.mock import patch, MagicMock
from src.extract import fetch_game_data

@patch("src.extract.requests.get")
def test_fetch_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "730": {"success": True, "data": {"name": "CS2"}}
    }
    mock_get.return_value = mock_response

    result = fetch_game_data(730)
    assert result == {"name": "CS2"}

@patch("src.extract.requests.get")
def test_fetch_not_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"999": {"success": False}}
    mock_get.return_value = mock_response

    result = fetch_game_data(999)
    assert result is None