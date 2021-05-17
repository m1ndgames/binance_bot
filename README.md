## binance_bot
A binance bot that watches a configured crypto pair and buys/sells according to price changes which can be freely
configured. The buy/sell actions are sent to a configurable Telegram channel.

The bot is configured and controlled via a web UI which runs on the localhost address. If you plan to access it remotely,
 for example via a reverse proxy, please make sure to implement some form of authentication (something like htaccess basic
auth)

### How does it work?
The bot checks the price of a given trading pair when a timer timer loop ends, if it changed above/below the configured
change limit, a buy/sell counter is created. When this counter reaches it's configured value, an order may be placed in
case the price is not higher than the defined max buy price.

It also includes a buy barrier function that saves the last sell price and adds a "red candle" size to it. This makes
sure the bot won't buy above this value. (You can define red candle size as 0 to deactivate this function)

Example:
* Sell price is 2.00 USDT
* Red candle size is 0.25

The buy barrier is now 1.75 - The bot will not buy again till the price drops below this value. I added this feature after
my bot bought at the top and unfortunately it had to stay there for a couple of days. :)

On the other hand, you don't want the bot to stay below this value for eternity in case the coin stays at the new high.
To counter this a buy barrier timer can be activated. When this timer is reached, the buy barrier
will be raised according to the defined value till it reaches the configured maximum price.

Example:
* Buy barrier is 1.75
* Buy barrier step size is 0.05
* Buy barrier timer is 3600 (One hour in seconds)
* Coin price is 2.00
* Max price is 5.00

If active, the buy barrier timer function will increase the barrier by 0.05 to 1.80, then 1.85, 1.90, and so on till it
either placed a buy order, or the max price is reached. After placing the buy order the new buy barrier is set as described
in the previous example, and the cycle starts over.

### Config
* Install python requirements: ``pip3 install -r requirements.txt``
* Start the bot: ```python3 run.py```
* Access the web UI on ``http://127.0.0.1:5311/config`` (See the pop-ups for explanation)

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

### Screenshots
#### Home
![No Connection](screenshots/binance_bot_screenshot_home.png?raw=true)
#### Config
![No Connection](screenshots/binance_bot_screenshot_config.png?raw=true)
#### Stats
![No Connection](screenshots/binance_bot_screenshot_stats.png?raw=true)

### Known issues / bugs
The bot relies on buy data to define the sell price. This means that you should not start this bot when you already have
the configured crypto currency on the exchange. Else it will potentially buy more using available funds, and then work
with any crypto currency available - defining the sell price for this asset as it has recorded himself.

### Donations
If you like my work and want to send me some coins along, please use this ADA address:
``addr1q8rt5wfhnuqtq74h5e9979nrz3rjsp9wdn7sdu5qhr992pcg7ts5v7g4suczxcku4385nm546hwaag853pm4ykf07ghqeakkk0``
