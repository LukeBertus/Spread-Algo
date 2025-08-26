# **2025 QFin Sem 2 Project**

## **Introduction**

In this project, your team is tasked with creating a trading bot that will run in a simulated market environment alongside some NPC bots in a turn-based fashion (i.e., all bots in the environment, including yours, are called in a cycle to interact with the market). In the first round, there will only be one market for a product called "UEC". In future rounds, there may be more products.

## **Data Structures**

All data sent between your bot and the exchange will use specific formats/classes. There are 5 (optionally 6) classes you should familiarize yourself with:

- `Msg`
- `Order`
- `Trade`
- `Product`
- `Rest`
- `Exchange` (optional)

## **Your Bot**

The template file for your bot can be found in `your_algo.py`. Your task involves modifying the `PlayerAlgorithm` class to make your bot execute your desired strategy.

Your bot will receive information in two forms:

### 1. **During Your Turn** (`send_messages` method)
- Your bot's `send_messages` method will be called with the current resting orderbook as input
- The orderbook will be comprised of resting orders represented as `Rest` objects
- You must return a list of messages to send back to the exchange
- These messages can be of two types:
  - `Order` - to place new orders
  - `Remove` - to cancel existing orders
- Each message is wrapped with the `Msg` class before being sent to the exchange

### 2. **After Trades** (`process_trades` method)
- At the end of each bot's turn, if any trades were made, your bot's `process_trades` method will be called with a list of trades as input
- The list of trades will contain `Trade` objects
- **Important**: You cannot send or remove orders during this method call
- However, you may modify any market tracking variables present in your `PlayerAlgorithm` class in preparation for your next `send_messages` call

## **Game Flow**

Below is a simplified version of the game flow:

```python
for _ in range(num_timesteps):
    for bot in bots:   # All bots in the market (including yours)
        messages = bot.send_messages(game.book)
        trades = []
        for msg in messages:
            trade = exchange.send(msg)  # send the message to the Exchange, gets trade, or None back
            if trade is not None:
                trades.append(trade)
        for bot in bots:
            bot.process_orders(trades)  # sends all the completed trades to the other bots
```

## **Market Maker Behavior**

One of the NPC bots in the market is a market maker bot. To provide liquidity, the market maker quotes at a constant width and density about some midprice. Orders are refreshed on each turn of the market maker bot.

The midprice that the orders are centered about is a function of the net position of the market maker. Particularly, it does this in a manner so that the market maker updates as if it would if it quoted infinitely many levels.

### **Example: Initial Market Maker Quotes**

| Price  | Bid Size | Ask Size |
|:------:|:--------:|:--------:|
| 105.00 |          | 25       |
| 104.50 |          | 25       |
| 104.00 |          | 25       |
| 103.50 |          | 25       |
| 102.50 | 25       |          |
| 102.00 | 25       |          |
| 101.50 | 25       |          |
| 101.00 | 25       |          |

### **After 25 Size is Bought from Market Maker**

If 25 size was bought from the Market Maker, the mid would then shift to 103.50, and when next refreshed the market maker would be quoting:

| Price  | Bid Size | Ask Size |
|:------:|:--------:|:--------:|
| 105.50 |          | 25       |
| 105.00 |          | 25       |
| 104.50 |          | 25       |
| 104.00 |          | 25       |
| 103.00 | 25       |          |
| 102.50 | 25       |          |
| 102.00 | 25       |          |
| 101.50 | 25       |          |

**Note**: The quoting is of constant size at every level, and the levels are evenly spaced. Additionally, the market maker has what is called a linear fade.

### **After 13 Size is Bought (Linear Fade Example)**

If 13 size was now bought from the market maker, the mid would then shift up by 26c to 103.76, so the MM would now quote:

| Price  | Bid Size | Ask Size |
|:------:|:--------:|:--------:|
| 105.76 |          | 25       |
| 105.26 |          | 25       |
| 104.76 |          | 25       |
| 104.26 |          | 25       |
| 103.26 | 25       |          |
| 102.76 | 25       |          |
| 102.26 | 25       |          |
| 101.76 | 25       |          |

## **Settlement**

Excess position does not just settle at the final bid/ask. To prevent the (very dumb) strategy of buying heaps to force the price up and finishing with final price > average trade price, settlement is conducted by determining what the average price would be if all the size remaining was traded against the market maker given the final price.

Given the relative position limits, this doesn't have a huge effect, but something to consider.

## **Fines**

There is no hard set position limit. However, at the end of every cycle, for every 1 position over the limit of 200, your bot will be fined $20. This is very significant relative to the total PnL in the game, so be careful with this.

## **Getting Started**

1. Follow `USAGE.md` to get set up
2. Create methods for tracking order IDs, and play around with sending/cancelling orders
3. Think about how to visualize the data
4. Implement a method of tracking your current position
5. Think about how you can export price data to a Jupyter notebook for better analysis

## **Tips and Tricks**

1. **Think about overfitting**: How will you determine the expected PnL of a trading strategy when applied to new data?
2. **Read through the different methods** thoroughly
3. **Consult with mentors**: The correlation between trading team competition performance and engagement with mentors is very high
4. **Submit something for the preliminary round**
5. **Learn classes**: If you are not familiar with classes/have never directly interacted with them, talk with your mentors/me as becoming comfortable interacting with the market is key

## **Reporting Bugs**

This is the first time this exact project has been run. P(∃ Bugs) ≈ 0.99, so please let me know if you notice anything. In the `game.py` file (which you do not have access to), this code is included that will print every time you run the simulation:

```python
random_seed = random.randint(0, 10000000)
random.seed(random_seed)
np.random.seed(random_seed)

print("Random seed set to:", random_seed)
```

**When reporting bugs, please include:**
- All of your code
- The random seed that was used

This will allow me to recreate the error if necessary.

## **Submission**

### **Format**

Email a single file to `qfinorderbot@gmail.com` containing your `PlayerAlgorithm` class. Ensure that your bot has:

- `bot.name` attribute with your team name
- `bot.team_members` attribute with a list containing the names of your team members

**Email subject must be:**
- `f"Project1 Submission_{team_name}"` or 
- `f"Preliminary1 Submission_{team_name}"`

### **Important Dates**

- **Preliminary Submission**: Midnight on the 20th of August
- **Final Submission**: Midnight on the 28th of August

**Note**: Preliminary submission is not compulsory but it will:
- Give you a reasonable sense for how your bot is doing relative to others
- Allow us to provide some feedback → we can generally provide feedback but can do so more formally and give you the potential to update your bots
- This is probably the only time that I (Josh) will do a full read-through and review of a bot as opposed to answering more specific questions, so take advantage of this

## **Assessment**

I do not like variance. As such, when assessing the bots I will run them many times (~20 each) on an additional 20k "rounds" and take the average PnL. 

**Performance Warning**: If the average running time is > 2 minutes per iteration, I will deduct some number of points. I do not believe this is preventing anything that you would want to do anyway, but if this is causing problems, please send your code to your mentor/Me/Sithum and we can have a look at it. Note that the base code with no expanded your_algo takes ~35s on my machine -> you may need to scale your time based on this, especially as this code seems to run quite slowly on Windows machines.

**Note**: This assessment function 𝔼[PnL] may change for future rounds. SIG recently did one of these with the loss function of 𝔼[PnL] - 0.1 × STD[PnL] that seemed reasonable, so just pay attention for future weeks.

## **Scoring**

- **Final Submission**: There will be a pool of 800 points awarded to teams with PnL > 0, awarded proportionally to the number of points you get
- **Preliminary Submission**: The same thing, but the pool size is 200 points


