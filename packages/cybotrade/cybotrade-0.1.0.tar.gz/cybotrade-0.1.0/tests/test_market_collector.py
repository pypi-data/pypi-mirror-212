from cybotrade.market_collector import MarketCollector
from datetime import datetime
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
async def test_market_collector_listen_candle():
    collector = await MarketCollector.connect([{ "exchange": "bybit_linear", "environment": "mainnet" }])
    assert hasattr(collector, "connect")
    assert hasattr(collector, "subscribe_candle")
    assert hasattr(collector, "listen_candle")

    await collector.subscribe_candle("BTC", "USDT", "1m", "bybit_linear", None)

    candle = await collector.listen_candle()
    assert schema(unified_candle) == candle
