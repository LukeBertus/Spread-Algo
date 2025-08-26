from typing import List
from time import time


class Msg:
    def __init__(self, msg_type, message):
        self.msg_type = msg_type
        self.message = message

class Order:
    """
    Order object containing a limit order with a. self.agg_dir is just the direction of the order
    """

    def __init__(self, ticker: str, price: float, size: int, order_id: int, agg_dir: str, bot_name: str):

        self.mapping = {"Buy": 1, "Sell": -1}
        if agg_dir not in self.mapping:
            raise ValueError(f"Invalid agg_dir: {agg_dir}. Must be 'Buy' or 'Sell'.")

        if size < 0 or int(size) != size:
            print(size, bot_name)
            raise ValueError("Size must be a positive integer.")
        
        
        self.ticker = ticker
        self.price = price
        self.size = size
        self.order_id = order_id # An order needs to be sent with a unique integer value order id. More details in PlayerAlgorithm
        self.agg_dir = agg_dir
        self.bot_name = bot_name
        self.aggness = self.price * self.mapping[self.agg_dir]

    def __str__(self):
        return f'{self.bot_name} wants to {self.agg_dir} at {self.price}' # Feel free to play with this if you want to


class Trade:
    """
    Trade object for record-keeping executed trades.
    """
    def __init__(self, price: float, size: int, ticker: str,
                 agg_order_id: int, rest_order_id: int,
                 agg_dir: str, agg_bot: str, rest_bot: str):
        self.ticker = ticker
        self.price = price
        self.size = size
        self.agg_order_id = agg_order_id
        self.agg_dir = agg_dir
        self.rest_order_id = rest_order_id
        self.trade_time = time()
        self.agg_bot = agg_bot # bot names not the bot object itself
        self.rest_bot = rest_bot

    def __str__(self):
        return f'{self.ticker} traded at {self.price}' # Feel free to play with this if you want to


class Product:
    """
    Product metadata container (tick size, limits, etc.)
    """
    def __init__(self, ticker: str, mpv: float = 1, lot_size: int = 1,
                 pos_limit=None, min_price=0, max_price=None, conversions=None, fine=0):
        self.ticker = ticker
        self.pos_limit = pos_limit
        self.min_price = min_price
        self.max_price = max_price
        self.mpv = mpv
        self.fine = fine
        self.lot_size = lot_size
        self.conversions = conversions or {}

    def __str__(self):
        return self.ticker
    
    def set_lore(self, lore):
        self.lore = lore # Call this, have a look
        

class Rest:
    """
    Resting order in the order book.
    """
    def __init__(self, size: int, price: float, dir, order_id: int,
                 ticker: str, aggness: float, bot_name: str):
        self.size = size
        self.rest_dir = dir
        self.price = price
        self.order_id = order_id
        self.ticker = ticker
        self.aggness = aggness
        self.bot_name = bot_name

    def __str__(self):
        return f"Price: {self.price}, Size: {self.size}"


class Exchange:
    """
    Exchange object. An exchange can hold a variety of products
    """
    def __init__(self, products: List[Product]):
        self.products = products
        self.ticker_to_product = {p.ticker: p for p in self.products}
        self.book = {p.ticker: {"Bids": [], "Asks": []} for p in self.products} # This will be stored most aggressive -> least aggressive
        self.trade_log = []
        self.mapping = {"Buy": 1, "Sell": -1}
        self.name_mapping = {"Buy": "Bids", "Sell": "Asks"}
        self.order_ids = {}  # order_id → [ticker, side] to allow for removal
        self.action_log = []
    
    def process_order(self, order: Order, loop_num=None) -> List[Trade]:

        if order.order_id in self.order_ids.keys():
            raise ValueError("Already Seen OrderId. Please ensure that a new OrderId has been generated")
        
        trades = []
        book = self.book[order.ticker]
        side_mapping = {"Buy": "Asks", "Sell": "Bids"}

        side_to_match = side_mapping[order.agg_dir]

        opposing_book = book[side_to_match]
        while order.size > 0 and opposing_book: # Finds the side of the book to check against

            rest_order = opposing_book[0] # extracts the top of book order
            price_match = (rest_order.price <= order.price) if order.agg_dir == "Buy" else (rest_order.price >= order.price) # Checks if the price matches
            if not price_match:
                break # clearly future orders will also not match

            trade_size = min(order.size, rest_order.size)

            trade = self.record_trade(rest_order.price, trade_size, order, rest_order)
            trades.append(trade)

            order.size -= trade_size
            rest_order.size -= trade_size

            if rest_order.size == 0:
                opposing_book.pop(0)

        if order.size > 0:
            self.add_order(order)

        return trades

    def record_trade(self, price: float, size: int, order: Order, rest: Rest) -> Trade: # These are the trade objects that your bot will process
        trade = Trade(
            price=price,
            size=size,
            ticker=order.ticker,
            agg_order_id=order.order_id,
            rest_order_id=rest.order_id,
            agg_dir=order.agg_dir,
            agg_bot=order.bot_name,
            rest_bot=rest.bot_name
        )

        """
        Returns a Trade object, and appends this to the trade log
        """
        self.trade_log.append(trade)
        return trade

    def remove_order(self, order_id: int) -> bool:
        """
        Need the order_id to cancel an order. Have stored the path in self.order_ids

        Returns True if the order was successfully removed, False otherwise.
        """
        info = self.order_ids.get(order_id)
        if not info:
            return False
        ticker, side = info
        book = self.book[ticker][side]
        for idx, rest in enumerate(book):
            if rest.order_id == order_id:
                book.pop(idx)
                return True
        return False

    def add_order(self, order: Order):
        """
        Adds an order to the order book, called after ensuring that it can not trade against any of the orders in the book
        """
        
        self.order_ids[order.order_id] = [order.ticker, self.name_mapping[order.agg_dir]] # mapping to help with removal
        rest = Rest(order.size, order.price, order.agg_dir, order.order_id, order.ticker,
                    order.price * self.mapping[order.agg_dir], order.bot_name)

        book = self.book[order.ticker]["Bids"] if order.agg_dir == "Buy" else self.book[order.ticker]["Asks"]

        for idx, item in enumerate(book):
            if order.aggness > item.aggness:
                book.insert(idx, rest)
                return
            elif order.aggness == item.aggness:
                insert_idx = idx
                while insert_idx + 1 < len(book) and book[insert_idx + 1].aggness == order.aggness:
                    insert_idx += 1
                book.insert(insert_idx + 1, rest)
                return

        book.append(rest)

