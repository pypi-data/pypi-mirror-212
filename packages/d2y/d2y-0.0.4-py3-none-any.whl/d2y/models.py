from dataclasses import dataclass, asdict
from d2y.enums import *
from datetime import datetime
from typing import List, Optional


@dataclass
class Profile:
    """
    Dataclass representing a user's profile info.

    Attributes:
    wallet_address (str): The address of the user's wallet.
    username (str): The username of the user.
    """    
    wallet_address: str
    username: str


@dataclass
class Account:
    """
    Dataclass representing a user's account info.

    Attributes:
    equity (float): Total value of the account.
    initial_margin (float): Initial margin required for the account.
    maintenance_margin (float): Maintenance margin required for the account.
    available_balance (float): Current available balance in the account.
    """    
    equity: float
    initial_margin: float
    maintenance_margin: float
    available_balance: float

@dataclass
class Portfolio:
    """
    Dataclass representing a user's portfolio info.

    Attributes:
    live_pnl (float): Live Profit and Loss value.
    win_rate (float): Winning rate of the portfolio.
    realized_pnl (float): Realized Profit and Loss value.
    profit_factor (float): Profit factor of the portfolio.
    margin_used (float): Margin used by the portfolio.
    mm_utilization (float): Margin utilization.
    gamma (float): Gamma of the portfolio.
    delta (float): Delta of the portfolio.
    theta (float): Theta of the portfolio.
    vega (float): Vega of the portfolio.
    rho (float): Rho of the portfolio.
    """    
    live_pnl: float
    win_rate: float
    realized_pnl: float
    profit_factor: float
    margin_used: float
    mm_utilization: float
    gamma: float
    delta: float
    theta: float
    vega: float
    rho: float

@dataclass
class Transfer:
    """
    Dataclass representing a deposit/withdrawal.

    Attributes:
    id (int): The unique identifier of the transfer.
    asset (str): The asset being transferred.
    transfer_type (TransferType): The type of transfer (e.g., DEPOSIT, WITHDRAW).
    amount (float): The amount of asset being transferred.
    tx_hash (str): The transaction hash of the transfer.
    created_at (str): The timestamp when the transfer was created.
    status (TransferStatus): The status of the transfer (e.g., PENDING, COMPLETED).
    """    
    id: int
    asset: str
    transfer_type: TransferType
    amount: float
    tx_hash: str
    created_at: str
    status: TransferStatus


@dataclass
class Asset:
    """
    Dataclass representing an asset.

    Attributes:
    id (int): The unique identifier of the asset.
    total_open_interest (float): The total open interest of the asset.
    notional_volume_24h (float): The notional volume of the asset in the last 24 hours.
    expiration_timestamps (List[str]): The expiration timestamps of the asset.
    total_options_open_interest (float): The total options open interest of the asset.
    total_futures_open_interest (float): The total futures open interest of the asset.
    options_notional_volume_24h (float): The options notional volume of the asset in the last 24 hours.
    futures_notional_volume_24h (float): The futures notional volume of the asset in the last 24 hours.
    name (str): The name of the asset.
    ticker (str): The ticker of the asset.
    underlying_price (float): The underlying price of the asset.
    underlying_price_updated_at (str): The timestamp when the underlying price was last updated.
    """    
    id: int
    total_open_interest: float
    notional_volume_24h: float
    expiration_timestamps: List[str]
    total_options_open_interest: float
    total_futures_open_interest: float
    options_notional_volume_24h: float
    futures_notional_volume_24h: float
    name: str
    ticker: str
    underlying_price: float
    underlying_price_updated_at: str


@dataclass
class SimpleInstrument:
    """
    Dataclass representing a instrument (simplified).

    Attributes:
    id (int): The unique identifier of the instrument.
    expiration_timestamp (str): The expiration timestamp of the instrument.
    asset (str): The asset that the instrument is related to.
    instrument_name (str): The name of the instrument.
    instrument_type (str): The type of the instrument.
    strike_price (Optional[float]): The strike price of the instrument (if applicable).
    option_type (Optional[OptionType]): The type of option (if the instrument is an option).
    """    
    id: int
    expiration_timestamp: str
    asset: str
    instrument_name: str
    instrument_type: str
    strike_price: Optional[float] = None
    option_type: Optional[OptionType] = None


@dataclass
class BBA:
    """
    Dataclass representing the best bid or bsk.

    Attributes:
    id (int): The unique identifier of the BBA.
    instrument (SimpleInstrument): The instrument associated with the BBA.
    average_price_matched (float): The average price matched in the BBA.
    price (float): The price of the BBA.
    quantity (float): The quantity in the BBA.
    quantity_filled (int): The quantity filled in the BBA.
    side (OrderSide): The side of the BBA (BUY or SELL).
    created_at (str): The timestamp when the BBA was created.
    status (OrderStatus): The status of the BBA.
    order_type (OrderType): The type of the BBA.
    is_liquidation (bool): Whether the BBA is a liquidation or not.
    user (int): The identifier of the user who placed the BBA.
    """    
    id: int
    instrument: SimpleInstrument
    average_price_matched: float
    price: float
    quantity: float
    quantity_filled: int
    side: OrderSide
    created_at: str
    status: OrderStatus
    order_type: OrderType
    is_liquidation: bool
    user: int

@dataclass
class BidAsk:
    """
    Dataclass representing a bid or ask.

    Attributes:
    price (float): The price of the bid or ask.
    quantity (float): The quantity of the bid or ask.
    """    
    price: float
    quantity: float

@dataclass
class Instrument:
    """
    Dataclass representing an instrument.

    Attributes:
    id (int): The unique identifier of the instrument.
    asset (str): The asset related to the instrument.
    instrument_name (str): The name of the instrument.
    mark_price (float): The mark price of the instrument.
    expiration_timestamp (str): The expiration timestamp of the instrument.
    settlement_period (str): The settlement period of the instrument.
    mark_price_updated_at (str): The timestamp when the mark price was last updated.
    mark_price_iv (float): The implied volatility at the mark price.
    created_at (str): The timestamp when the instrument was created.
    instrument_type (str): The type of the instrument.
    strike_price (Optional[float]): The strike price of the instrument (if applicable).
    option_type (Optional[str]): The type of option (if the instrument is an option).
    underlying_price_at_expiration (Optional[float]): The underlying price of the instrument at its expiration.
    best_bid (Optional[BBA]): The best bid for the instrument.
    best_ask (Optional[BBA]): The best ask for the instrument.
    open_interest (Optional[float]): The open interest of the instrument.
    implied_volatility_bids (Optional[float]): The implied volatility of the bids for the instrument.
    implied_volatility_asks (Optional[float]): The implied volatility of the asks for the instrument.
    delta (Optional[float]): The delta of the instrument.
    vega (Optional[float]): The vega of the instrument.
    gamma (Optional[float]): The gamma of the instrument.
    rho (Optional[float]): The rho of the instrument.
    theta (Optional[float]): The theta of the instrument.
    """    
    id: int
    asset: str
    instrument_name: str
    mark_price: float
    expiration_timestamp: str
    settlement_period: str
    mark_price_updated_at: str
    mark_price_iv: float
    created_at: str
    instrument_type: str
    strike_price: Optional[float] = None
    option_type: Optional[str] = None
    underlying_price_at_expiration: Optional[float] = None
    best_bid: Optional[BBA] = None
    best_ask: Optional[BBA] = None
    open_interest: Optional[float] = None
    implied_volatility_bids: Optional[float] = None
    implied_volatility_asks: Optional[float] = None
    delta: Optional[float] = None
    vega: Optional[float] = None
    gamma: Optional[float] = None
    rho: Optional[float] = None
    theta: Optional[float] = None


@dataclass
class Orderbook:
    """
    Dataclass representing an orderbook.

    Attributes:
    bids (List[BidAsk]): The list of bids in the orderbook.
    asks (List[BidAsk]): The list of asks in the orderbook.
    """    
    bids: List[BidAsk]
    asks: List[BidAsk]


@dataclass
class Order:
    """
    Dataclass requivalent to an order.

    Attributes:
    id (int): The unique identifier of the order.
    instrument (SimpleInstrument): The instrument associated with the order.
    average_price_matched (float): The average price matched in the order.
    price (float): The price of the order.
    quantity (float): The quantity in the order.
    quantity_filled (float): The quantity filled in the order.
    side (OrderSide): The side of the order (BUY or SELL).
    created_at (str): The timestamp when the order was created.
    status (OrderStatus): The status of the order.
    order_type (OrderType): The type of the order.
    is_liquidation (bool): Whether the order is a liquidation or not.
    user (int): The identifier of the user who placed the order.
    """
    id: int
    instrument: SimpleInstrument
    average_price_matched: float
    price: float
    quantity: float
    quantity_filled: float
    side: OrderSide
    created_at: str
    status: OrderStatus
    order_type: OrderType
    is_liquidation: bool
    user: int

@dataclass
class OrderInput:
    """
    Dataclass representing an order input.

    Attributes:
    quantity (int): The quantity of the order.
    side (OrderSide): The side of the order (BUY or SELL).
    order_type (OrderType): The type of the order.
    price (Optional[float]): The price of the order.
    instrument_id (Optional[int]): The identifier of the instrument associated with the order.
    instrument_name (Optional[str]): The name of the instrument associated with the order.
    """
    quantity: int
    side: OrderSide
    order_type: OrderType
    price: Optional[float] = None
    instrument_id: Optional[int] = None
    instrument_name: Optional[str] = None

@dataclass
class Trade:
    """
    Dataclass representing a trade.

    Attributes:
    created_at (str): The timestamp when the trade was created.
    instrument (Instrument): The instrument associated with the trade.
    price (float): The price of the trade.
    quantity (float): The quantity in the trade.
    order_type (Optional[OrderType]): The type of the order associated with the trade.
    order_side (Optional[OrderSide]): The side of the order associated with the trade.
    pnl (Optional[float]): The profit and loss of the trade.
    fees (Optional[float]): The fees of the trade.
    is_maker (Optional[bool]): Whether the trade was a maker or not.
    taker_side (Optional[OrderSide]): The side of the taker order associated with the trade.
    """
    created_at: str
    instrument: Instrument
    price: float
    quantity: float
    order_type: Optional[OrderType] = None
    order_side: Optional[OrderSide] = None
    pnl: Optional[float] = None
    fees: Optional[float] = None
    is_maker: Optional[bool] = None
    taker_side: Optional[OrderSide] = None


@dataclass
class Position:
    """
    Dataclass representing a position.

    Attributes:
    instrument (Instrument): The instrument associated with the position.
    position (float): The position.
    average_entry_price (float): The average entry price of the position.
    created_at (str): The timestamp when the position was created.
    """
    
    instrument: Instrument
    position: float
    average_entry_price: float
    created_at: str
