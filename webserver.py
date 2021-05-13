import bottle
from database import DatabaseManager


class Webserver:
    def __init__(self, bot=None):
        self.bot = bot
        self.database = DatabaseManager(self)

    # Define Sites
    def index(self):
        return bottle.template('index')

    def config(self):
        return bottle.template('config', pair=self.database.read_config()[0],
                               base_asset=self.database.read_config()[1],
                               quote_asset=self.database.read_config()[2],
                               change_limit=self.database.read_config()[3],
                               minimum_profit=self.database.read_config()[4],
                               take_profit=self.database.read_config()[5],
                               max_price=self.database.read_config()[6],
                               redcandle_size=self.database.read_config()[7],
                               timer=self.database.read_config()[8],
                               buy_trigger=self.database.read_config()[9],
                               sell_trigger=self.database.read_config()[10],
                               testmode=self.database.read_config()[11],
                               binance_apikey=self.database.read_config()[12],
                               binance_apikey_secret=self.database.read_config()[13],
                               telegram_active=self.database.read_config()[14],
                               telegram_apikey=self.database.read_config()[15],
                               telegram_channel_id=self.database.read_config()[16])

    def saveconfig(self):
        pair = bottle.request.forms.get('pair')
        base_asset = bottle.request.forms.get('base_asset')
        quote_asset = bottle.request.forms.get('quote_asset')
        change_limit = bottle.request.forms.get('change_limit')
        minimum_profit = bottle.request.forms.get('minimum_profit')
        take_profit = bottle.request.forms.get('take_profit')
        max_price = bottle.request.forms.get('max_price')
        redcandle_size = bottle.request.forms.get('redcandle_size')
        timer = bottle.request.forms.get('timer')
        buy_trigger = bottle.request.forms.get('buy_trigger')
        sell_trigger = bottle.request.forms.get('sell_trigger')
        testmode = bottle.request.forms.get('testmode')
        binance_apikey = bottle.request.forms.get('binance_apikey')
        binance_apikey_secret = bottle.request.forms.get('binance_apikey_secret')
        telegram_active = bottle.request.forms.get('telegram_active')
        telegram_apikey = bottle.request.forms.get('telegram_apikey')
        telegram_channel_id = bottle.request.forms.get('telegram_channel_id')

        self.database.write_config(pair, base_asset, quote_asset, change_limit, minimum_profit, take_profit, max_price,
                              redcandle_size, timer, buy_trigger, sell_trigger, testmode, binance_apikey,
                              binance_apikey_secret, telegram_active, telegram_apikey, telegram_channel_id)

        return bottle.template('saveconfig', msg="Config saved successfully")

    def stats(self):
        orders = self.database.read_all_orders()
        return bottle.template('stats', orders=orders)

    def start(self):
        web = Webserver()

        # Routes
        bottle.route("/")(web.index)
        bottle.route("/config")(web.config)
        bottle.route("/saveconfig", method='POST')(web.saveconfig)
        bottle.route("/stats")(web.stats)

        # Start Webserver
        bottle.run(host='127.0.0.1', port=5311)

