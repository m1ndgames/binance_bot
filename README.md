## binance_bot
A binance bot that watches a configured crypto pair and buys/sells according to price changes which can be freely
configured. The buy/sell actions are sent to a configurable Telegram channel.

### Config
````
[token]
pair           = ADAUSDT    # The Pair (for example BTCUSDT)
token          = ADA        # Token (BTC)
currency       = USDT       # Currency (USDT) - Can also be ETH or whatever pair is used.

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
apikey         = <binance api key>
apikey_secret  = <binance secret api key>

[telegram]
active         = true
apikey         = <bot token>
channel_id     = <telegram channel id>
````

### Telegram Setup
If configured, you need to create a Telegram channel and a bot.

* Create the application: https://my.telegram.org/apps
* Create a Telegram channel
* Receive the channel id like this:
````
    Go to https://web.telegram.org/
    Click on your channel
    Look at the URL and find the part that looks like c12112121212_17878787878787878
    Remove the underscore and after c12112121212
    Remove the prefixed letter 12112121212
    Prefix with a -100 so -10012112121212
    That's your channel id.
````
* Create a bot with Botfather (https://core.telegram.org/bots) and receive the bot token
* Invite the bot to your channel

### Bugs / Improvements
If you find a bug or have a feature request please open a github issue.

### Contact
You can reach me via Discord: m1ndgames#1337

### Donations
If you like my work and want to send me some coins along, please use this ADA address:
``addr1q8rt5wfhnuqtq74h5e9979nrz3rjsp9wdn7sdu5qhr992pcg7ts5v7g4suczxcku4385nm546hwaag853pm4ykf07ghqeakkk0``
