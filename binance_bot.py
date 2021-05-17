from binance.client import Client
from binance.enums import *
from webserver import Webserver
from database import DatabaseManager
import configparser
import time
import math
import requests
#from threading import Thread
import threading
from datetime import datetime


class BinanceBot:
    def __init__(self):
        super().__init__()
        self.webserver = Webserver(self)
        self.database = DatabaseManager(self)

        # Init variables
        self.config = {}
        self.binance = None
        self.trading_pair_info = None
        self.base_asset_name = None
        self.base_asset_precision = None
        self.base_asset_balance = None
        self.base_asset_balance_precision = None
        self.base_asset_price = None
        self.base_asset_sell_price = None
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
        self.countdown_timer = None
        self.buy_barrier_countdown_timer = None
        self.buy_barrier_timer_thread = None
        self.telegram = None
        self.sell_counter = 0
        self.buy_counter = 0
        self.timer_thread = None
        self.trading_thread = None
        self.webserver_thread = None

    def refresh_config(self):
        # Read config from database
        self.config['pair'] = self.database.read_config()[0]
        self.config['base_asset'] = self.database.read_config()[1]
        self.config['quote_asset'] = self.database.read_config()[2]
        self.config['change_limit'] = self.database.read_config()[3]
        self.config['minimum_profit'] = self.database.read_config()[4]
        self.config['take_profit'] = self.database.read_config()[5]
        self.config['max_price'] = self.database.read_config()[6]
        self.config['redcandle_size'] = self.database.read_config()[7]
        self.config['timer'] = self.database.read_config()[8]
        self.config['buy_trigger'] = self.database.read_config()[9]
        self.config['sell_trigger'] = self.database.read_config()[10]
        self.config['testmode'] = self.database.read_config()[11]
        self.config['binance_apikey'] = self.database.read_config()[12]
        self.config['binance_apikey_secret'] = self.database.read_config()[13]
        self.config['telegram_active'] = self.database.read_config()[14]
        self.config['telegram_apikey'] = self.database.read_config()[15]
        self.config['telegram_channel_id'] = self.database.read_config()[16]
        self.config['buy_barrier_step_size'] = self.database.read_config()[17]
        self.config['buy_barrier_timer'] = self.database.read_config()[18]
        self.config['buy_barrier_timer_enabled'] = self.database.read_config()[19]

        # Stop if missing config values
        if not self.config['pair']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['base_asset']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['quote_asset']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['change_limit']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['minimum_profit']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['take_profit']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['max_price']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['redcandle_size']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['timer']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['buy_trigger']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['sell_trigger']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['testmode']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['binance_apikey']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if not self.config['binance_apikey_secret']:
            self.output(text="Config incomplete - Set all values in the WebUI!", telegram=False, log=False)
            return
        if self.config['telegram_active'] == 'on' and not self.config['telegram_apikey']:
            self.output(text="Telegram activated but no API key provided!", telegram=False, log=False)
            self.config['telegram_active'] = 'off'
        if self.config['telegram_active'] == 'on' and not self.config['telegram_channel_id']:
            self.output(text="Telegram activated but no channel ID provided!", telegram=False, log=False)
            self.config['telegram_active'] = 'off'

        # Binance Client
        self.binance = Client(self.config['binance_apikey'], self.config['binance_apikey_secret'])
        self.trading_pair_info = self.binance.get_symbol_info(self.database.read_config()[0])
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

    def setup(self):
        # Setup the database
        self.database.setup_database()

        # Load config
        self.refresh_config()

        # Start timer thread
        self.timer_thread = threading.Thread(target=self.timer, daemon=True, name='timer')
        self.timer_thread.start()

        # Start bot thread
        self.trading_thread = threading.Thread(target=self.trading, daemon=True, name='bot')
        self.trading_thread.start()

    def timer(self):
        countdown = int(self.config['timer'])
        while countdown > -1:
            time.sleep(1)
            countdown -= 1
            if countdown == -1:
                countdown = int(self.config['timer'])
            self.countdown_timer = countdown

    def output(self, text: str = None, telegram: bool = False, log: bool = False):
        now = datetime.now()
        time_string = now.strftime("%d/%m/%Y %H:%M:%S")

        print(str(time_string) + "\t\t" + str(text))

        if self.config['telegram_active'] == 'on':
            if telegram:
                requests.get("https://api.telegram.org/bot" + str(self.config['telegram_apikey']) + "/sendMessage?chat_id=" + str(self.config['telegram_channel_id']) + "&text=" + str(text))

        if log:
            f = open("binance_bot.log", "a")
            f.write(str(time_string) + " - " + text + "\n")
            f.close()

    def get_price(self):
        try:
            prices = self.binance.get_all_tickers()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        pair = self.database.read_config()[0]
        for asset in prices:
            if asset['symbol'] == pair:
                price = asset['price']
                return price

    def round_step_size(self, quantity, step_size):
        precision = int(round(-math.log(float(step_size), 10), 0))
        return float(round(float(quantity), precision))

    def floor_step_size(self, quantity, step_size):
        precision = int(round(-math.log(step_size, 10), 0))
        return int(quantity*(10**precision)) / (10**precision)

    def sell_order(self, amount: float = None, price: float = None):
        if amount and price:
            rounded = self.floor_step_size(float(amount), float(self.pair_step_size))
            if self.config['testmode'] == 'on':
                self.output(text="Test sell-order triggered")
            else:
                try:
                    order = self.binance.create_order(
                        symbol=self.database.read_config()[0],
                        side=SIDE_SELL,
                        type=ORDER_TYPE_LIMIT,
                        timeInForce=TIME_IN_FORCE_GTC,
                        newOrderRespType=ORDER_RESP_TYPE_FULL,
                        quantity=rounded,
                        price=price)
                    if order:
                        # Write sell data to database
                        self.database.write_sell_data(str(self.trading_pair_info['symbol']), str(self.base_asset_name), str(self.quote_asset_name), float(price), float(rounded))

                        return True
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

    def buy_order(self, amount: float = None):
        if amount:
            rounded = self.floor_step_size(float(amount), float(self.pair_step_size))

            if self.config['testmode'] == 'on':
                self.output(text="Test buy-order triggered", telegram=True)
            else:
                try:
                    order = self.binance.order_market_buy(symbol=self.database.read_config()[0], quoteOrderQty=rounded, newOrderRespType=ORDER_RESP_TYPE_FULL)
                    if order:
                        if order['status'] == 'FILLED':
                            if order['fills']:
                                for fill in order['fills']:
                                    buy_price = fill['price']

                                    # Write buy order to database
                                    self.database.write_buy_data(self.trading_pair_info['symbol'], self.base_asset_name, self.quote_asset_name, buy_price, rounded)
                                    return True
                except requests.exceptions.RequestException as e:
                    raise SystemExit(e)

    def cancel_open_orders(self):
        try:
            orders = self.binance.get_open_orders(symbol=self.database.read_config()[0])
            if orders:
                for o in orders:
                    if o['status'] != 'FILLED':
                        self.binance.cancel_order(symbol=self.database.read_config()[0], orderId=o['orderId'])
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def check_buy_barrier_timer(self):
        if self.config['buy_barrier_timer_enabled'] == 'on':
            if not self.buy_barrier_timer_thread:
                self.buy_barrier_timer_thread = threading.Thread(target=self.buy_barrier_timer, daemon=True, name='buy_barrier_timer')
                self.buy_barrier_timer_thread.start()

    def buy_barrier_timer(self):
        while getattr(self.buy_barrier_timer_thread, "run", True):
            buy_barrier_timer = int(self.config['buy_barrier_timer'])
            while buy_barrier_timer > -1:
                if self.config['buy_barrier_timer_enabled'] == 'off':
                    self.buy_barrier_timer_thread = None
                    self.buy_barrier_countdown_timer = None
                    exit(0)

                time.sleep(1)
                buy_barrier_timer -= 1
                if buy_barrier_timer == -1:
                    self.update_buy_barrier_by_timer()
                    buy_barrier_timer = int(self.config['buy_barrier_timer'])
                self.buy_barrier_countdown_timer = buy_barrier_timer

    def update_buy_barrier_by_timer(self):
        if self.config['buy_barrier_timer_enabled'] == 'on':
            if not self.database.is_selling():
                if self.database.read_buy_barrier() > 0 and self.database.read_buy_barrier() <= (float(self.config['max_price'] - self.config['buy_barrier_step_size'])):
                    current_buy_barrier = self.database.read_buy_barrier()
                    new_buy_barrier = current_buy_barrier + self.config['buy_barrier_step_size']
                    self.database.update_buy_barrier(new_buy_barrier)
                    self.output(text="Buy Barrier has been increased by " + self.config['buy_barrier_step_size'] + " from " + current_buy_barrier + " to " + new_buy_barrier, telegram=False, log=True)

    def trading(self):
        while True:
            if self.countdown_timer == 0:
                # Update config each tick
                self.refresh_config()

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
                if self.database.read_last_buy_order_price():
                    self.base_asset_buy_price = self.database.read_last_buy_order_price()
                else:
                    self.base_asset_buy_price = None

                # Define Sell/Take-Profit Prices
                if self.base_asset_buy_price:
                    self.base_asset_sell_price = self.base_asset_buy_price + float(self.config['minimum_profit'])
                    self.base_asset_take_profit_price = self.base_asset_buy_price + float(self.config['take_profit'])

                # Calculate Buy/Sell Trigger
                check_change = self.base_asset_change
                if check_change < 0:
                    check_change = check_change * -1

                if self.base_asset_change > 0 and check_change > float(self.config['change_limit']):
                    self.sell_counter = self.sell_counter + 1
                    self.buy_counter = 0
                elif self.base_asset_change < 0 and check_change > float(self.config['change_limit']):
                    self.buy_counter = self.buy_counter + 1
                    self.sell_counter = 0

                # Sell Logic
                if self.database.is_selling() == 1:
                    if self.base_asset_take_profit_price < self.base_asset_price and self.base_asset_balance['free'] > self.pair_min_quantity:
                        sell_order = self.sell_order(self.base_asset_balance['free'], self.base_asset_price)
                        if sell_order:
                            rounded = (float(self.base_asset_balance['free']) // float(self.pair_step_size)) * float(self.pair_step_size)
                            self.output(text="Sold " + str(rounded) + " " + self.base_asset_name + " for " + str(self.base_asset_price) + " " + self.quote_asset_name + " - Total: " + str(rounded * self.base_asset_price) + " " + self.quote_asset_name, telegram=True, log=True)

                    elif self.base_asset_sell_price < self.base_asset_price and self.base_asset_balance['free'] > self.pair_min_quantity and self.sell_counter >= int(self.config['sell_trigger']):
                        sell_order = self.sell_order(self.base_asset_balance['free'], self.base_asset_price)
                        if sell_order:
                            rounded = (float(self.base_asset_balance['free']) // float(self.pair_step_size)) * float(self.pair_step_size)
                            self.output(text="Sold " + str(rounded) + " " + self.base_asset_name + " for " + str(self.base_asset_price) + " " + self.quote_asset_name + " - Total: " + str(rounded * self.base_asset_price) + " " + self.quote_asset_name, telegram=True, log=True)

                #  Buy Logic
                else:
                    if self.quote_asset_balance['free'] > self.pair_min_quantity and self.buy_counter >= int(self.config['buy_trigger']) and self.base_asset_price < float(self.config['max_price']):
                        if self.database.read_buy_barrier() > 0:
                            if self.base_asset_price < self.database.read_buy_barrier():
                                buy_order = self.buy_order(float(self.quote_asset_balance_precision))
                                if buy_order:
                                    try:
                                        new_base_asset_balance = self.binance.get_asset_balance(asset=self.base_asset_name)
                                    except requests.exceptions.RequestException as e:
                                        raise SystemExit(e)

                                    self.output(text="Bought " + str(new_base_asset_balance['free']) + " " + self.base_asset_name + " for " + str(self.quote_asset_balance_precision) + " " + self.quote_asset_name + " at " + str(self.base_asset_price) + " " + str(self.quote_asset_name), telegram=True, log=True)
                        else:
                            buy_order = self.buy_order(float(self.quote_asset_balance_precision))
                            if buy_order:
                                try:
                                    new_base_asset_balance = self.binance.get_asset_balance(asset=self.base_asset_name)
                                except requests.exceptions.RequestException as e:
                                    raise SystemExit(e)

                                self.output(text="Bought " + str(new_base_asset_balance['free']) + " " + self.base_asset_name + " for " + str(self.quote_asset_balance_precision) + " " + self.quote_asset_name + " at " + str(self.base_asset_price) + " " + str(self.quote_asset_name), telegram=True, log=True)

                # End the loop
                self.base_asset_old_price = self.base_asset_price

            time.sleep(1)

    def run(self):
        # Set variables
        self.setup()

        self.output(text="binance_bot started", telegram=True, log=True)

        # Show warning if testmode is active
        if self.config['testmode'] == 'on':
            self.output(text="Warning: Testmode is active - orders wont be processed.", telegram=True)

        # Start webserver
        self.webserver_thread = threading.Thread(target=self.webserver.run, daemon=True, name='webserver')
        self.webserver_thread.start()

        while True:
            time.sleep(1)
            # This function handles the Buy Barrier Countdown and starts and stops the thread as needed
            self.check_buy_barrier_timer()

            # Restart crashed threads
            if not self.trading_thread.is_alive():
                self.output(text="binance_bot crashed - restarting thread", telegram=True, log=True)
                self.trading_thread = threading.Thread(target=self.trading, daemon=True, name='bot')
                self.trading_thread.start()

            if not self.timer_thread.is_alive():
                self.timer_thread = threading.Thread(target=self.timer, daemon=True, name='timer')
                self.timer_thread.start()

            # Stop program and kill all threads when we stop the bottle webserver
            if not self.webserver_thread.is_alive():
                self.output(text="binance_bot stopped", telegram=True, log=True)
                exit(0)
