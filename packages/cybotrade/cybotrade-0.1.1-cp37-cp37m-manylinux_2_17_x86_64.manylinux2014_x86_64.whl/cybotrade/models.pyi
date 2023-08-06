from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Symbol:
    base: str
    quote: str

@dataclass
class Candle:
    symbol: Symbol
    open: float
    high: float
    low: float
    close: float
    volume: float
    trade_count: Optional[float]
    is_closed: bool
    exchange: Exchange
    start_time: datetime
    end_time: datetime

@dataclass
class ExchangeConfig:
    exchange: Exchange
    environment: Environment

@dataclass
class OrderBookSubscriptionParams:
    depth: int
    speed: Optional[int]
    extra_params: Optional[dict[str, str]]

@dataclass
class Level:
    price: float
    quantity: float

@dataclass
class LocalOrderBookUpdate:
    best_bid: float
    bids: List[Level]
    best_ask: float
    asks: List[Level]
    spread: float
    depth: int
    exchange: Exchange

@dataclass
class OrderResponse:
    exchange: Exchange
    exchange_order_id: str
    client_order_id: str

@dataclass
class OrderUpdate:
    symbol: Symbol
    order_type: OrderType
    side: OrderSide
    time_in_force: TimeInForce
    exchange_order_id: str
    order_time: datetime
    updated_time: datetime
    size: float
    filled_size: float
    remain_size: float
    price: float
    client_order_id: str
    status: OrderStatus
    exchange: Exchange
    is_reduce_only: bool
    is_hedge_mode: bool

@dataclass
class Position:
    symbol: Symbol
    quantity: float
    value: float
    entry_price: float
    cumulative_realized_pnl: Optional[float]
    unrealized_pnl: float
    liquidation_price: float
    position_side: PositionSide
    margin: Optional[PositionMargin]
    initial_margin: float
    leverage: float
    exchange: Exchange

@dataclass
class Balance:
    exchange: Exchange
    coin: str
    wallet_balance: float
    available_balance: float
    initial_margin: Optional[float]
    margin_balance: Optional[float]
    maintenance_margin: Optional[float]

@dataclass
class Order:
    exchange_order_id: str
    client_order_id: str
    symbol: Optional[str]
    time_in_force: Optional[TimeInForce]
    side: Optional[OrderSide]
    order_type: Optional[OrderType]
    exchange: Exchange
    price: float
    quantity: float
    is_reduce_only: Optional[bool]

class Exchange(Enum):
    BinanceSpot = 0
    BinanceLinear = 1
    BinanceInverse = 2
    BybitSpot = 3
    BybitLinear = 4
    BybitInverse = 5
    OkxSpot = 6
    OkxLinear = 7
    OkxInverse = 8
    KucoinSpot = 9
    KucoinLinear = 10
    KucoinInverse = 11
    GateIoSpot = 12
    GateIoLinear = 13
    GateIoInverse = 14
    ZoomexLinear = 15
    ZoomexInverse = 16

class Environment(Enum):
    Testnet = 0
    Demo = 1
    Mainnet = 2

class OrderSide(Enum):
    Buy = 0
    Sell = 1

class OrderType(Enum):
    Market = 0
    Limit = 1

class OrderStatus(Enum):
    Created = 0
    PartiallyFilled = 1
    PartiallyFilledCancelled = 2
    Filled = 3
    Cancelled = 4
    Rejected = 5
    CancelRejected = 6

class TimeInForce(Enum):
    GTC = 0
    IOC = 1
    FOK = 2
    PostOnly = 3

class PositionSide(Enum):
    Closed = 0
    OneWayLong = 1
    OneWayShort = 2
    HedgeLong = 3
    HedgeShort = 4

class PositionMargin(Enum):
    Cross = 0
    Isolated = 1

class Interval(Enum):
    OneMinute = 0
    ThreeMinute = 1
    FiveMinute = 2
    FifteenMinute = 3
    ThirtyMinute = 4
    OneHour = 5
    TwoHour = 6
    FourHour = 7
    SixHour = 8
    TwelveHour = 9
    OneDay = 10
    ThreeDay = 11
    OneWeek = 12
    OneMonth = 13
