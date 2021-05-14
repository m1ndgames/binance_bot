import bottle
import json


class Webserver:
    def __init__(self, bot):
        self.bot = bot

    # Define Sites
    def index(self):
        return bottle.template('index',
                               countdown=self.bot.countdown_timer,
                               pair=self.bot.config['pair'],
                               base_asset_name=self.bot.base_asset_name,
                               base_asset_price=self.bot.base_asset_price,
                               quote_asset_name=self.bot.quote_asset_name,
                               base_asset_balance_precision=self.bot.base_asset_balance_precision,
                               quote_asset_balance_precision=self.bot.quote_asset_balance_precision)

    def config(self):
        return bottle.template('config', pair=self.bot.database.read_config()[0],
                               base_asset=self.bot.database.read_config()[1],
                               quote_asset=self.bot.database.read_config()[2],
                               change_limit=self.bot.database.read_config()[3],
                               minimum_profit=self.bot.database.read_config()[4],
                               take_profit=self.bot.database.read_config()[5],
                               max_price=self.bot.database.read_config()[6],
                               redcandle_size=self.bot.database.read_config()[7],
                               timer=self.bot.database.read_config()[8],
                               buy_trigger=self.bot.database.read_config()[9],
                               sell_trigger=self.bot.database.read_config()[10],
                               testmode=self.bot.database.read_config()[11],
                               binance_apikey=self.bot.database.read_config()[12],
                               binance_apikey_secret=self.bot.database.read_config()[13],
                               telegram_active=self.bot.database.read_config()[14],
                               telegram_apikey=self.bot.database.read_config()[15],
                               telegram_channel_id=self.bot.database.read_config()[16])

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

        self.bot.database.write_config(pair, base_asset, quote_asset, change_limit, minimum_profit, take_profit, max_price,
                              redcandle_size, timer, buy_trigger, sell_trigger, testmode, binance_apikey,
                              binance_apikey_secret, telegram_active, telegram_apikey, telegram_channel_id)

        return bottle.template('saveconfig', msg="Config saved successfully")

    def stats(self):
        orders = self.bot.database.read_all_orders()
        return bottle.template('stats', orders=orders)

    def api(self, path=None):
        if path == "asset_data":
            return json.dumps({'countdown_timer': self.bot.countdown_timer,
                               'pair': self.bot.config['pair'],
                               'base_asset_name': self.bot.base_asset_name,
                               'base_asset_price': self.bot.base_asset_price,
                               'quote_asset_name': self.bot.quote_asset_name,
                               'base_asset_balance_precision': self.bot.base_asset_balance_precision,
                               'quote_asset_balance_precision': self.bot.quote_asset_balance_precision,
                               'buy_barrier': self.bot.database.read_buy_barrier()
                               })
        else:
            return 0

    def run(self):
        web = Webserver(self.bot)

        # Routes
        bottle.route("/")(web.index)
        bottle.route("/config")(web.config)
        bottle.route("/saveconfig", method='POST')(web.saveconfig)
        bottle.route("/stats")(web.stats)
        bottle.route("/api/<path>")(web.api)

        # Start Webserver
        bottle.run(server='wsgiref', host='127.0.0.1', port=5311, quiet=True)

