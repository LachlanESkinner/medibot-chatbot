import pytest
from main import get_coordinates, fetch_weather
import aiohttp

@pytest.mark.asyncio
async def test_fetch_weather_invalid_api_key(monkeypatch):
    class MockResponse:
        status = 401

        async def json(self):
            return {}

        async def text(self):
            return "Unauthorized"

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

    class MockSession:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        def get(self, url, params=None):
            return MockResponse()

    monkeypatch.setattr(aiohttp, "ClientSession", lambda *args, **kwargs: MockSession())

    location = "Cambridge"
    lat, lon = get_coordinates(location)
    result = await fetch_weather(location, lat, lon)

    assert "error" in result
