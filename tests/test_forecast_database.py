import sys
import os
import pytest
pytestmark = pytest.mark.asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from main import fetch_and_store_forecast, get_forecast_from_db

def test_forecast_storage_and_retrieval():
    location = "Bristol"
    success = fetch_and_store_forecast(location)
    assert success == True

    forecasts = get_forecast_from_db(location)
    assert len(forecasts) > 0
    for forecast in forecasts:
        assert hasattr(forecast, "temp")
        assert hasattr(forecast, "description")
