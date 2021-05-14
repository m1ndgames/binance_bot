## binance_bot
A binance bot that watches a configured crypto pair and buys/sells according to price changes which can be freely
configured. The buy/sell actions are sent to a configurable Telegram channel.

The bot is configured and controlled via a web UI which runs on the localhost address. If you plan to access it remotely
via a reverse proxy, please make sure to implement some form of authentication (for example something like htaccess basic
auth)

### Config
* Install python requirements: ``pip3 install -r requirements.txt``
* Start the bot: ```python3 run.py```
* Access the web UI on ``http://127.0.0.1:5311/config``

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

### Known issues / bugs
The bot relies on buy data to define the sell price. This means that you should not start this bot when you already have
crypto currency on the exchange. Else it will potentially buy more using available funds, and then work with any
crypto currency available - defining the sell price for this asset as it has recorded himself.

### Donations
If you like my work and want to send me some coins along, please use this ADA address:
``addr1q8rt5wfhnuqtq74h5e9979nrz3rjsp9wdn7sdu5qhr992pcg7ts5v7g4suczxcku4385nm546hwaag853pm4ykf07ghqeakkk0``
