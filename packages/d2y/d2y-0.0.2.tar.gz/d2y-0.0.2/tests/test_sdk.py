import unittest
import os
from dotenv import load_dotenv
from sdk import Client
from enums import *
from models import *

load_dotenv()

API_KEY = 'cKVG7-0KTcGpBiCJ4Zb993zxZeX245eIGv4rc0JAskU'
API_SECRET = 'fvTxXGpE8XLkDiJPFn_uSrXpo4cJI1RDaiHX3B8NNCY'

# API_KEY = os.environ["API_KEY"]
# API_SECRET = os.environ["API_SECRET"]
BASE_URL = os.environ.get("API_BASE_URL", "https://api.dev.d2y.exchange")

TEST_OPTION_ID = os.environ.get("TEST_OPTION_ID", 167704)
TEST_OPTION_STRIKE_PRICE = float(os.environ.get("TEST_OPTION_STRIKE_PRICE", 1600))
TEST_OPTION_EXPIRATION_TIMESTAMP = os.environ.get(
    "TEST_OPTION_EXPIRATION_TIMESTAMP", "2023-06-02T08:00:00Z"
)


class TestTradingClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sdk = TradingClient(api_key=API_KEY, api_secret=API_SECRET, base_url=BASE_URL)

    def test_get_profile(self):
        print("\n****** GETTING USER PROFILE ******\n")
        profile = self.sdk.get_profile()
        print("\n****** Profile:", profile)
        for key, value in profile.__dict__.items():
            print(f"{key}: {value}")

    def test_get_account(self):
        print("\n****** GETTING ACCOUNT ******\n")
        account = self.sdk.get_account()
        print("Account:", account)
        for key, value in account.__dict__.items():
            print(f"{key}: {value}")

    def test_get_transfers(self):
        print("\n****** GETTING Transfers ******\n")
        transfers = self.sdk.get_transfers()
        print("Transfers:", transfers)
        for transfer in transfers:
            print("Transfer:", transfer)
            for key, value in transfer.__dict__.items():
                print(f"{key}: {value}")        

    def test_portfolio(self):
        print("\n****** GETTING PORTFOLIO ******\n")
        portfolio = self.sdk.get_portfolio()
        print("Portfolio:", portfolio)
        for key, value in portfolio.__dict__.items():
            print(f"{key}: {value}")

    def test_get_assets(self):
        print("\n****** GETTING ASSETS ******\n")
        assets = self.sdk.get_assets()
        for asset in assets:
            print("Asset:", asset)
            for key, value in asset.__dict__.items():
                print(f"{key}: {value}")


    def test_get_markets(self):
        print("\n****** GETTING MARKETS ******\n")
        markets = self.sdk.get_markets(
            expiration_timestamp=[TEST_OPTION_EXPIRATION_TIMESTAMP],
            option_type=OptionType.CALL,
            strike_price=[TEST_OPTION_STRIKE_PRICE],
            instrument_type=InstrumentType.OPTION,
        )
        for market in markets:
            print("Market:", market)
            for key, value in market.__dict__.items():
                print(f"{key}: {value}")

    def test_get_orderbook(self):
        print("\n****** GETTING ORDERBOOK ******\n")
        orderbook = self.sdk.get_orderbook(instrument_id=TEST_OPTION_ID)
        print("Orderbook for option_id:", orderbook)

    def test_get_orders(self):
        print("\n****** GETTING ORDERS ******\n")
        orders = self.sdk.get_orders(status=[OrderStatus.OPEN], limit=3, offset=0)
        for order in orders[:3]:
            print("Order:", order)
            for key, value in order.__dict__.items():
                print(f"{key}: {value}")

    def test_cancel_all_orders(self):
        print("\n****** CANCELING ALL ORDERS ******\n")
        cancellation_result = self.sdk.cancel_all_orders(
            # expiration_timestamp=TEST_OPTION_EXPIRATION_TIMESTAMP,
            # instrument_id=TEST_OPTION_ID,
            # instrument_name=TEST_OPTION_NAME,
            # instrument_type=InstrumentType.OPTION,
            strike_price=1600
        )
        print("Cancellation Result:", cancellation_result)
        for key, value in cancellation_result.items():
            print(f"{key}: {value}")

    def test_reduce_order(self):
        print("\n****** REDUCING ORDER ******\n")
        order_id = 187921  # Replace with the actual order ID
        reduced_order_result = self.sdk.reduce_order(order_id=order_id, quantity=.5)
        print("Reduced Order Result:", reduced_order_result)
        for key, value in reduced_order_result.items():
            print(f"{key}: {value}")


    def test_get_positions(self):
        print("\n****** GETTING POSITIONS ******\n")
        positions = self.sdk.get_positions()
        for position in positions:
            print("Position:", position)
            for key, value in position.__dict__.items():
                print(f"{key}: {value}")

    def test_get_trades(self):
        print("\n****** GETTING TRADES ******\n")
        trades = self.sdk.get_trades()
        for trade in trades:
            print("Trade:", trade)
            for key, value in trade.__dict__.items():
                print(f"{key}: {value}")

    def test_post_orders_and_cancel_order(self):
        print("\n****** POSTING AND CANCELING ORDER ******\n")
        new_order = self.sdk.place_order(
            instrument_id=TEST_OPTION_ID,
            price=0.01,
            quantity=2,
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT
        )
        print("Order:", new_order)
        for key, value in new_order.__dict__.items():
            print(f"{key}: {value}")

        print("\n****** CANCELLING ORDER ******\n")
        cancel_order = self.sdk.cancel_order(new_order.id)
        print("Cancelled order:", cancel_order)
        # for key, value in cancel_order.__dict__.items():
        #     print(f"{key}: {value}")

    def test_post_multi_orders_and_get_trades(self):
        print("\n****** POSTING BULK ORDERS ******\n")
        orders = self.sdk.place_bulk_order([
            {
                "instrument_id": TEST_OPTION_ID,
                "price": 0.01,
                "quantity": 1,
                "side": OrderSide.BUY,
                "order_type": OrderType.LIMIT,
            },
            {
                "instrument_id": TEST_OPTION_ID,
                "quantity": 1,
                "side": OrderSide.SELL,
                "order_type": OrderType.MARKET,
            },
        ])
        for order in orders:
            print("Order:", order)
            for key, value in order.__dict__.items():
                print(f"{key}: {value}")



if __name__ == "__main__":
    unittest.main()