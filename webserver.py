import bottle
import json
from bottle import static_file


class Webserver:
    def __init__(self, bot):
        self.bot = bot

    # Define Sites
    def home(self):
        return bottle.template('home',
                               countdown=self.bot.countdown_timer,
                               is_selling=self.bot.database.is_selling()
                               )

    def config(self):
        return bottle.template('config',
                               countdown=self.bot.countdown_timer,
                               pair=self.bot.database.read_config()[0],
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
                               telegram_channel_id=self.bot.database.read_config()[16],
                               is_selling=self.bot.database.is_selling(),
                               buy_barrier=self.bot.database.read_buy_barrier(),
                               buy_barrier_step_size=self.bot.database.read_config()[17],
                               buy_barrier_timer=self.bot.database.read_config()[18],
                               buy_barrier_timer_enabled=self.bot.database.read_config()[19]
                               )

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
        buy_barrier = bottle.request.forms.get('buy_barrier')
        buy_barrier_step_size = bottle.request.forms.get('buy_barrier_step_size')
        buy_barrier_timer = bottle.request.forms.get('buy_barrier_timer')
        buy_barrier_timer_enabled = bottle.request.forms.get('buy_barrier_timer_enabled')

        self.bot.database.write_config(pair, base_asset, quote_asset, change_limit, minimum_profit, take_profit,
                                       max_price, redcandle_size, timer, buy_trigger, sell_trigger, testmode,
                                       binance_apikey, binance_apikey_secret, telegram_active, telegram_apikey,
                                       telegram_channel_id, buy_barrier_step_size, buy_barrier_timer,
                                       buy_barrier_timer_enabled)

        if buy_barrier:
            self.bot.database.update_buy_barrier(buy_barrier)

        return bottle.template('saveconfig',
                               msg="Config saved successfully",
                               countdown=self.bot.countdown_timer,
                               is_selling=self.bot.database.is_selling()
                               )

    def stats(self):
        orders = self.bot.database.read_all_orders()
        return bottle.template('stats',
                               orders=orders,
                               countdown=self.bot.countdown_timer,
                               is_selling=self.bot.database.is_selling()
                               )

    def graph(self):
        return bottle.template('graph',
                               pair=self.bot.config['pair'],
                               countdown=self.bot.countdown_timer,
                               is_selling=self.bot.database.is_selling()
                               )

    def api(self, path=None):
        if path == "asset_data":
            return json.dumps({'countdown_timer': self.bot.countdown_timer,
                               'pair': self.bot.config['pair'],
                               'base_asset_name': self.bot.base_asset_name,
                               'base_asset_price': self.bot.base_asset_price,
                               'quote_asset_name': self.bot.quote_asset_name,
                               'base_asset_balance_precision': self.bot.base_asset_balance_precision,
                               'quote_asset_balance_precision': self.bot.quote_asset_balance_precision,
                               'buy_barrier': self.bot.database.read_buy_barrier(),
                               'base_asset_buy_price': self.bot.base_asset_buy_price,
                               'base_asset_sell_price': self.bot.base_asset_sell_price,
                               'base_asset_take_profit_price': self.bot.base_asset_take_profit_price,
                               'sell_counter': self.bot.sell_counter,
                               'sell_trigger': self.bot.config['sell_trigger'],
                               'buy_counter': self.bot.buy_counter,
                               'buy_trigger': self.bot.config['buy_trigger'],
                               'base_asset_change': self.bot.base_asset_change
                               })

        elif path == "log":
            reader = open('binance_bot.log', 'r')
            try:
                output = {}
                output['log_lines'] = {}
                id = 1
                lines = reader.readlines()
                for line in lines:
                    output['log_lines'][id] = line
                    id = id + 1

                output['line_count'] = id
                return json.dumps(output)
            finally:
                reader.close()
        else:
            return 0

    def serve_static(self, filename):
        return static_file(filename, root='./static')

    def serve_img(self, filename):
        return static_file(filename, root='./img')

    def run(self):
        web = Webserver(self.bot)

        # Routes
        bottle.route("/")(web.home)
        bottle.route("/config")(web.config)
        bottle.route("/saveconfig", method='POST')(web.saveconfig)
        bottle.route("/stats")(web.stats)
        bottle.route("/graph")(web.graph)
        bottle.route("/static/<filename:path>")(web.serve_static)
        bottle.route("/img/<filename>")(web.serve_img)
        bottle.route("/api/<path>")(web.api)

        # Start Webserver
        bottle.run(server='wsgiref', host='127.0.0.1', port=5311, quiet=True)
