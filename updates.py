def __init__(self, products):
        self.products = products       
        self.name = "PlayerAlgorithm"   
        self.timestamp_num = 0          

        self.positions["Cash"] = 0

        self.mapping = {"Buy": 1, "Sell": -1}


def process_trades(self, trades):

    for trade in trades:
        if trade.agg_bot == self.name:
            self.positions[trade.ticker] += trade.size * self.mapping[trade.agg_dir]
            self.positions["Cash"] -= trade.size * trade.price * self.mapping[trade.agg_dir]
        elif trade.rest_bot == self.name:
            self.positions[trade.ticker] -= trade.size * self.mapping[trade.agg_dir]  
            self.positions["Cash"] += trade.size * trade.price * self.mapping[trade.agg_dir]


# =================In play_game.py==============

pnl = player_bot.positions["Cash"]