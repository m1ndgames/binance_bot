from bottle import route, run, post, request, static_file
import database


class Webserver:
    def __init__(self, bot=None):
        self.bot = bot

    # Define Sites
    def index(self):
        return bottle.template('index')

    def config(self):
        configdata = database.read_config()
        return bottle.template('config', config=configdata)

    @post('/saveconfig')
    def saveconfig(self):
        msg = "Config saved succesfully"

        pair = request.forms.get('pair')
        if not pair:
            msg = "You need to specify a Trading Pair"
            return bottle.template('config_saved', msg=msg)

        base_asset = request.forms.get('base_asset')
        if not pair:
            msg = "You need to specify a Base Asset"
            return bottle.template('config_saved', msg=msg)

        quote_asset = request.forms.get('quote_asset')
        if not pair:
            msg = "You need to specify a Quote Asset"
            return bottle.template('config_saved', msg=msg)

        change_limit = request.forms.get('change_limit')
        if not pair:
            msg = "You need to specify a Change Limit"
            return bottle.template('config_saved', msg=msg)

        minimum_profit = request.forms.get('minimum_profit')
        if not pair:
            msg = "You need to specify the minimum profit"
            return bottle.template('config_saved', msg=msg)

        take_profit = request.forms.get('take_profit')
        if not pair:
            msg = "You need to specify the take profit value"
            return bottle.template('config_saved', msg=msg)

        max_price = request.forms.get('max_price')
        if not pair:
            msg = "You need to specify the maximum price"
            return bottle.template('config_saved', msg=msg)

        redcandle_size = request.forms.get('redcandle_size')
        if not pair:
            msg = "You need to specify the red candle size"
            return bottle.template('config_saved', msg=msg)

        timer = request.forms.get('timer')
        if not pair:
            msg = "You need to specify a timer"
            return bottle.template('config_saved', msg=msg)

        buy_trigger = request.forms.get('buy_trigger')
        if not pair:
            msg = "You need to specify a buy trigger"
            return bottle.template('config_saved', msg=msg)

        sell_trigger = request.forms.get('sell_trigger')
        if not pair:
            msg = "You need to specify a sell trigger"
            return bottle.template('config_saved', msg=msg)

        testmode = request.forms.get('testmode')

        binance_apikey = request.forms.get('binance_apikey')
        if not pair:
            msg = "You need to specify the Binance API key"
            return bottle.template('config_saved', msg=msg)

        binance_apikey_secret = request.forms.get('binance_apikey_secret')
        if not pair:
            msg = "You need to specify the Binance secret"
            return bottle.template('config_saved', msg=msg)

        telegram_active = request.forms.get('telegram_active')

        telegram_apikey = request.forms.get('telegram_apikey')
        if telegram_active and not not telegram_apikey:
            msg = "You need to specify the Telegram API key"
            return bottle.template('config_saved', msg=msg)

        telegram_channel_id = request.forms.get('telegram_channel_id')
        if telegram_active and not not telegram_channel_id:
            msg = "You need to specify Telegram channel ID"
            return bottle.template('config_saved', msg=msg)

        database.write_config(pair, base_asset, quote_asset, change_limit, minimum_profit, take_profit, max_price, redcandle_size, timer, buy_trigger, sell_trigger, testmode, binance_apikey, binance_apikey_secret, telegram_active, telegram_apikey, telegram_channel_id)
        return bottle.template('config_saved', msg=msg)

    def stats(self):
        orders = database.read_all_orders()
        return bottle.template('stats', orders=orders)

    def start(self):
        web = Webserver()

        # Routes
        bottle.route("/")(web.index)
        bottle.route("/config")(web.config)
        bottle.route("/stats")(web.stats)

        # Start Webserver
        bottle.run(host='127.0.0.1', port=8008)

