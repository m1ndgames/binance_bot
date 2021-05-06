# binance_bot
Another binance bot...

This was created just for fun, to see how well a bot can do with a little money running 24/7.

Use at your own risk!

# Config
````
[token]
pair     = ADAUSDT          # The Pair (for example BTCUSDT)
token    = ADA              # Token (BTC)
currency = USDT             # Currency (USDT) - Can also be ETH or whatever pair is used.

[base]
change_limit   = <FLOAT>    # If the coin prices changes by this amount, the buy/sell counter is raised.
minimum_profit = <FLOAT>    # The minimum profit per coin. The bot will sell when this is reached and sell counter is hit.
take_profit    = <FLOAT>    # If the price goes above buy price + take_profit, the bot sells no matter the counter.
max_price      = <FLOAT>    # The Max price of a coin, if its above the bot wont buy.
redcandle_size = <FLOAT>    # This is a buy barrier. If you define 0.1 the bot will buy when price reaches the last sell price - candle_size.
timer          = <INT>      # Delay in seconds in between each check.
buy_trigger    = <INT>      # How many times a coin value should go up (change_limit) before the bot buys.
sell_trigger   = <INT>      # How many times a coin value should go up (change_limit) before the bot sells.
testmode       = <0|1>      # If enabled, no orders are processed.

[binance]
apikey_public = <binance public api key>
apikey_private = <binance private api key>

[telegram]
apikey     = <telegram api key>
channel_id = <telegram channel id>