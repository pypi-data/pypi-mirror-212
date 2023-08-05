from cybotrade.datahub import Datahub
from datetime import datetime, timedelta
from os import environ
from pytest import mark
from pytest_schema import schema, Or

unified_candle = {
    "symbol": {
        "base": str,
        "quote": str,
    },
    "open": float,
    "high": float,
    "low": float,
    "close": float,
    "volume": float,
    "trade_count": Or(float, None),
    "is_closed": bool,
    "exchange": str,
    "start_time": datetime,
    "end_time": datetime,
}

@mark.asyncio
async def test_datahub_candle():
    url = environ.get("DATAHUB_URL")
    assert url != ""

    datahub = await Datahub.connect(url)
    assert hasattr(datahub, "connect")
    assert hasattr(datahub, "candle")

    candles = await datahub.candle("BTC", "USDT", "1m", "bybit_linear", datetime.utcnow() - timedelta(minutes=10), datetime.utcnow())
    assert len(candles) > 0
    assert schema([unified_candle]) == candles
