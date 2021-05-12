from binance.client import Client
from binance.enums import *
from webserver import Webserver
import database
import configparser
import time
import math
import requests
from threading import Thread
from datetime import datetime
from colorama import init, Fore, Style
init()


class BinanceBot:
    def __init__(self):
        super().__init__()
        self.webserver = Webserver(self)

        # Init variables
        self.config = configparser.ConfigParser()
        self.binance = None
        self.trading_pair_info = None
        self.base_asset_name = None
        self.base_asset_precision = None
        self.base_asset_balance = None
        self.base_asset_balance_precision = None
        self.base_asset_price = None
        self.base_asset_sell_price = None
        self.base_asset_previous_sell_price = None
        self.base_asset_take_profit_price = None
        self.base_asset_buy_price = None
        self.base_asset_old_price = None
        self.base_asset_change = None
        self.quote_asset_name = None
        self.quote_asset_precision = None
        self.quote_asset_balance = None
        self.quote_asset_balance_precision = None
        self.pair_min_price = None
        self.pair_max_price = None
        self.pair_min_quantity = None
        self.pair_max_quantity = None
        self.pair_step_size = None
        self.pair_min_ordersize = None
        self.order_change_limit = None
        self.order_redcandle_size = None
        self.order_minimum_profit = None
        self.order_take_profit = None
        self.order_max_price = None
        self.order_timer = None
        self.order_buy_trigger = None
        self.order_sell_trigger = None
        self.order_testmode = None
        self.telegram_active = None
        self.telegram_apikey = None
        self.telegram_channel_id = None
        self.countdown_timer = None
        self.telegram = None
        self.sell_counter = 0
        self.buy_counter = 0
        self.timer_thread = None
        self.bot_thread = None
        self.webserver_thread = None

    def setup(self):
        self.config.read('binance_bot.cfg')
        self.binance = Client(self.config['binance']['apikey'], self.config['binance']['apikey_secret'])
        self.trading_pair_info = self.binance.get_symbol_info(self.config['token']['pair'])

        self.base_asset_name = self.trading_pair_info['baseAsset']
        self.base_asset_precision = self.trading_pair_info['baseAssetPrecision']
        self.quote_asset_name = self.trading_pair_info['quoteAsset']
        self.quote_asset_precision = self.trading_pair_info['quoteAssetPrecision']

        for f in self.trading_pair_info['filters']:
            if f['filterType'] == 'PRICE_FILTER':
                self.pair_min_price = f['minPrice']
                self.pair_max_price = f['maxPrice']
            if f['filterType'] == 'LOT_SIZE':
                self.pair_min_quantity = f['minQty']
                self.pair_max_quantity = f['maxQty']
                self.pair_step_size = f['stepSize']
            if f['filterType'] == 'MIN_NOTIONAL':
                self.pair_min_ordersize = f['minNotional']

        self.order_change_limit = float(self.config['base']['change_limit'])
        self.order_minimum_profit = float(self.config['base']['minimum_profit'])
        self.order_take_profit = float(self.config['base']['take_profit'])
        self.order_max_price = float(self.config['base']['max_price'])
        self.order_timer = int(self.config['base']['timer'])
        self.order_buy_trigger = int(self.config['base']['buy_trigger'])
        self.order_sell_trigger = int(self.config['base']['sell_trigger'])
        self.order_testmode = int(self.config['base']['testmode'])
        self.order_redcandle_size = float(self.config['base']['redcandle_size'])

        self.telegram_active = self.config['telegram']['active']
        self.telegram_apikey = self.config['telegram']['apikey']
        self.telegram_channel_id = self.config['telegram']['channel_id']

        # Setup the database
        database.setup_database()

        # Start timer thread
        self.timer_thread = Thread(target=self.timer, daemon=True, name='timer')
        self.timer_thread.start()

        # Start bot thread
        self.bot_thread = Thread(target=self.bot, daemon=True, name='bot')
        self.bot_thread.start()

    def timer(self):
        countdown = self.order_timer
        while countdown > -1:
            time.sleep(1)
            countdown -= 1
            if countdown == -1:
                countdown = self.order_timer
            self.countdown_timer = countdown

    def output(self, level: str = "info", text: str = None, telegram: bool = False, log: bool = False):
        now = datetime.now()
        time_string = now.strftime("%d/%m/%Y %H:%M:%S")

        if level == 'info':
            color = Fore.GREEN
        elif level == 'warn':
            color = Fore.YELLOW
            log = True
        else:
            color = Fore.RED
            log = True
            telegram = True

        print(color + str(time_string) + Style.RESET_ALL + " - " + str(text) + Style.RESET_ALL)

        if self.telegram_active == 'true':
            if telegram:
                requests.get("https://api.telegram.org/bot" + str(self.telegram_apikey) + "/sendMessage?chat_id=" + str(self.telegram_channel_id) + "&text=" + str(text))

        if log:
            f = open("binance_bot.log", "a")
            f.write(str(time_string) + " - " + str(level) + " - " + text + "\n")
            f.close()

    def get_price(self):
        try:
            prices = self.binance.get_all_tickers()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        pair = self.config['token']['pair']
        for asset in prices:
            if asset['symbol'] == pair:
                price = asset['price']
                return price

    def status_message(self):
        if self.base_asset_change < 0:
            change_color = Fore.RED
        elif self.base_asset_change > 0:
            change_color = Fore.GREEN
        else:
            change_color = Style.RESET_ALL

        asset_line = "Wallet - " + self.base_asset_name + ": " + str(self.base_asset_balance_precision) + "\t" + self.quote_asset_name + ": " + self.quote_asset_balance_precision
        price_line = "Token  - Price: " + str(self.base_asset_price) + "\tChange: " + change_color + str(self.base_asset_change) + Style.RESET_ALL

        if database.is_selling() == 1:
            asset_line = asset_line + "\tBuy Price: " + str(self.base_asset_buy_price) + " - Sell Price: " + str(self.base_asset_sell_price) + " - Take profit at: " + str(self.base_asset_take_profit_price)
        if database.read_buy_barrier() != 0.0 and not database.is_selling():
            asset_line = asset_line + "\tBuying below " + str(database.read_buy_barrier() - self.order_redcandle_size)

        if self.sell_counter != 0 and self.base_asset_buy_price:
            price_line = price_line + "\tSell Counter: " + str(self.sell_counter) + "/" + str(self.order_sell_trigger)
        elif self.buy_counter != 0 and not self.base_asset_buy_price:
            price_line = price_line + "\tBuy Counter: " + str(self.buy_counter) + "/" + str(self.order_buy_trigger)

        self.output(text=asset_line, telegram=False, log=False)
        self.output(text=price_line, telegram=False, log=False)

    def round_step_size(self, quantity, step_size):
        precision = int(round(-math.log(float(step_size), 10), 0))
        return float(round(float(quantity), precision))

    def floor_step_size(self, quantity, step_size):
        precision = int(round(-math.log(step_size, 10), 0))
        return int(quantity*(10**precision)) / (10**precision)

    def sell_order(self, amount: float = None, price: float = None):
        if amount and price:
            rounded = self.floor_step_size(float(amount), float(self.pair_step_size))
            if self.order_testmode == 1:
                self.output(level="warn", text="Test sell-order triggered", telegram=False, log=False)
            else:
                try:
                    order = self.binance.create_order(
                        symbol=self.config['token']['pair'],
                        side=SIDE_SELL,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        newOrderRespType=ORDER_RESP_TYPE_FULL,
                        quantity=rounded,
                        price=price)
                    if order:
                        print(str(order))

                        # Write sell data to database
                        database.write_sell_data(str(self.trading_pair_info['symbol']), str(self.base_asset_name), str(self.quote_asset_name), float(price), float(rounded))

                        return True
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

    def buy_order(self, amount: float = None):
        if amount:
            rounded = (float(amount) // float(self.pair_step_size)) * float(self.pair_step_size)

            if self.order_testmode == 1:
                self.output(level="warn", text="Test buy-order triggered", telegram=True, log=False)
            else:
                try:
                    order = self.binance.order_market_buy(symbol=self.config['token']['pair'], quoteOrderQty=rounded, newOrderRespType=ORDER_RESP_TYPE_FULL)
                    if order:
                        print(str(order))
                        if order['status'] == 'FILLED':
                            if order['fills']:
                                for fill in order['fills']:
                                    buy_price = fill['price']

                                    # Write buy order to database
                                    database.write_buy_data(self.trading_pair_info['symbol'], self.base_asset_name, self.quote_asset_name, buy_price, rounded)
                                    return True
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

    def cancel_open_orders(self):
        try:
            orders = self.binance.get_open_orders(symbol=self.config['token']['pair'])
            if orders:
                for o in orders:
                    if o['status'] != 'FILLED':
                        self.binance.cancel_order(symbol=self.config['token']['pair'], orderId=o['orderId'])
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def bot(self):
        while True:
            if self.countdown_timer == 0:
                # Check open Orders which have not been processed
                # self.cancel_open_orders()

                # Gather current token data
                try:
                    self.base_asset_balance = self.binance.get_asset_balance(asset=self.base_asset_name)
                    self.quote_asset_balance = self.binance.get_asset_balance(asset=self.quote_asset_name)
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

                self.base_asset_balance_precision = "{:0.0{}f}".format(float(self.base_asset_balance['free']), int(self.base_asset_precision))
                self.quote_asset_balance_precision = "{:0.0{}f}".format(float(self.quote_asset_balance['free']), int(self.quote_asset_precision))
                self.base_asset_price = float(self.get_price())

                # Set old price initially and calculate the change from last loop
                if not self.base_asset_old_price:
                    self.base_asset_old_price = self.base_asset_price
                    self.base_asset_change = 0.0
                else:
                    self.base_asset_change = self.base_asset_price - self.base_asset_old_price

                # Check if we have a buy price
                if database.read_last_buy_order_price():
                    self.base_asset_buy_price = database.read_last_buy_order_price()
                else:
                    self.base_asset_buy_price = None

                # Define Sell/Take-Profit Prices
                if self.base_asset_buy_price:
                    self.base_asset_sell_price = self.base_asset_buy_price + self.order_minimum_profit
                    self.base_asset_take_profit_price = self.base_asset_buy_price + self.order_take_profit

                # Calculate Buy/Sell Trigger
                check_change = self.base_asset_change
                if check_change < 0:
                    check_change = check_change * -1

                if self.base_asset_change > 0 and check_change > self.order_change_limit:
                    self.sell_counter = self.sell_counter + 1
                    self.buy_counter = 0
                elif self.base_asset_change < 0 and check_change > self.order_change_limit:
                    self.buy_counter = self.buy_counter + 1
                    self.sell_counter = 0

                # Print status messages
                self.status_message()

                # Sell Logic
                if database.is_selling() == 1:
                    if self.base_asset_take_profit_price < self.base_asset_price and self.base_asset_balance['free'] > self.pair_min_quantity:
                        sell_order = self.sell_order(self.base_asset_balance['free'], self.base_asset_price)
                        if sell_order:
                            rounded = (float(self.base_asset_balance['free']) // float(self.pair_step_size)) * float(self.pair_step_size)
                            self.output(level="info", text=Fore.RED + "Sold " + Style.RESET_ALL + str(rounded) + " " + self.base_asset_name + " for " + str(self.base_asset_price) + " " + self.quote_asset_name, telegram=True, log=True)

                    elif self.base_asset_sell_price < self.base_asset_price and self.base_asset_balance['free'] > self.pair_min_quantity and self.sell_counter >= self.order_sell_trigger:
                        sell_order = self.sell_order(self.base_asset_balance['free'], self.base_asset_price)
                        if sell_order:
                            rounded = (float(self.base_asset_balance['free']) // float(self.pair_step_size)) * float(self.pair_step_size)
                            self.output(level="info", text=Fore.RED + "Sold " + Style.RESET_ALL + str(rounded) + " " + self.base_asset_name + " for " + str(self.base_asset_price) + " " + self.quote_asset_name, telegram=True, log=True)

                #  Buy Logic
                else:
                    if self.quote_asset_balance['free'] > self.pair_min_quantity and self.buy_counter >= self.order_buy_trigger and self.base_asset_price < self.order_max_price:
                        if database.read_last_sell_order_price():
                            if self.base_asset_price < (self.base_asset_previous_sell_price - self.order_redcandle_size):
                                buy_order = self.buy_order(float(self.quote_asset_balance_precision))
                                if buy_order:
                                    try:
                                        new_base_asset_balance = self.binance.get_asset_balance(asset=self.base_asset_name)
                                    except requests.exceptions.RequestException as e:
                                        raise SystemExit(e)

                                    self.output(level="info", text=Fore.GREEN + "Bought " + Style.RESET_ALL + str(new_base_asset_balance) + " " + self.base_asset_name + " for " + str(self.quote_asset_balance_precision) + " " + self.quote_asset_name, telegram=True, log=True)
                        else:
                            buy_order = self.buy_order(float(self.quote_asset_balance_precision))
                            if buy_order:
                                try:
                                    new_base_asset_balance = self.binance.get_asset_balance(asset=self.base_asset_name)
                                except requests.exceptions.RequestException as e:
                                    raise SystemExit(e)

                                self.output(level="info", text=Fore.GREEN + "Bought " + Style.RESET_ALL + str(new_base_asset_balance) + " " + self.base_asset_name + " for " + str(self.quote_asset_balance_precision) + " " + self.quote_asset_name, telegram=True, log=True)

                # End the loop
                self.base_asset_old_price = self.base_asset_price

            time.sleep(1)

    def run(self):
        # Set variables
        self.setup()

        self.output(level="info", text="binance_bot started", telegram=True, log=True)

        # Show warning if testmode is active
        if self.order_testmode == 1:
            self.output(level="warn", text="Warning: Testmode is active - orders wont be processed.", telegram=True, log=False)

        # Start webserver
        self.webserver_thread = Thread(target=self.webserver.start(), daemon=True, name='webserver')
        self.webserver_thread.start()

        while True:
            time.sleep(1)

            # Restart crashed threads
            if not self.bot_thread.is_alive():
                self.output(level="warn", text="binance_bot crashed - restarting thread", telegram=True, log=True)
                self.bot_thread = Thread(target=self.bot, daemon=True, name='bot')
                self.bot_thread.start()

            if not self.timer_thread.is_alive():
                self.timer_thread = Thread(target=self.timer, daemon=True, name='timer')
                self.timer_thread.start()

            # Stop program and kill all threads when we stop the bottle webserver
            if not self.webserver_thread.is_alive():
                exit(0)
