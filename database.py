import datetime
import sqlite3
from datetime import datetime

sql_buy_table = """ CREATE TABLE IF NOT EXISTS buy_history (
                                        id INTEGER PRIMARY KEY,
                                        pair string,
                                        base_asset string,
                                        quote_asset string,
                                        price float,
                                        total float,
                                        date INTEGER
                                    ); """

sql_sell_table = """ CREATE TABLE IF NOT EXISTS sell_history (
                                        id INTEGER PRIMARY KEY,
                                        pair string,
                                        base_asset string,
                                        quote_asset string,
                                        price float,
                                        total float,
                                        date INTEGER
                                    ); """

sql_state_table = """ CREATE TABLE IF NOT EXISTS state (
                                        sell_active INTEGER,
                                        buy_barrier float
                                    ); """

sql_config_table = """ CREATE TABLE IF NOT EXISTS config (
                                        pair string,
                                        base_asset string,
                                        quote_asset string,
                                        change_limit float,
                                        minimum_profit float,
                                        take_profit float,
                                        max_price float,
                                        redcandle_size float,
                                        timer int,
                                        buy_trigger int,
                                        sell_trigger int,
                                        testmode string,
                                        binance_apikey string,
                                        binance_apikey_secret string,
                                        telegram_active string,
                                        telegram_apikey string,
                                        telegram_channel_id string
                                    ); """


class DatabaseManager:
    def __init__(self, bot):
        self.bot = bot

    def setup_database(self):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        try:
            print("Connected to sqlite db v." + str(sqlite3.version))
            self.create_table(db, sql_buy_table)
            self.create_table(db, sql_sell_table)
            self.create_table(db, sql_state_table)
            self.create_table(db, sql_config_table)

            # Check if we need to setup state data on first launch
            cursor = db.cursor()
            cursor.execute('SELECT 1 FROM state LIMIT 1')
            state_data_exists = cursor.fetchone() is not None
            if not state_data_exists:
                setup_state_data = """INSERT INTO 'state'
                                          ('sell_active', 'buy_barrier') 
                                          VALUES (?, ?);"""

                init_data = (0, 0)
                cursor.execute(setup_state_data, init_data)
                db.commit()

            # Check if we need to setup config data on first launch
            cursor.execute('SELECT 1 FROM config LIMIT 1')
            config_data_exists = cursor.fetchone() is not None
            if not config_data_exists:
                setup_config_data = """INSERT INTO 'config'
                                              ('pair', 'base_asset', 'quote_asset', 'change_limit', 'minimum_profit',
                                              'take_profit', 'max_price', 'redcandle_size', 'timer', 'buy_trigger',
                                              'sell_trigger', 'testmode', 'telegram_active') 
                                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

                init_data = ('ADAUSDT', 'ADA', 'USDT', 0.001, 0.02, 0.04, 1.9, 0.04, 10, 3, 3, "on", "off")
                cursor.execute(setup_config_data, init_data)
                db.commit()

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_sql)

        except sqlite3.Error as e:
            print(e)

    def write_sell_data(self, pair: str, base_asset: str, quote_asset: str, price: float, total: float):
        """ Write sell data """
        db = sqlite3.connect(r"binance_bot.sqlite")
        try:
            cursor = db.cursor()
            sqlite_insert_with_param = """INSERT INTO 'sell_history'
                                      ('pair', 'base_asset', 'quote_asset', 'price', 'total', 'date') 
                                      VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (pair, base_asset, quote_asset, price, total, datetime.now())

            cursor.execute(sqlite_insert_with_param, data_tuple)
            db.commit()

            self.update_sell_state(0)
            self.update_buy_barrier(price - self.read_config()[7])

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

    def write_buy_data(self, pair: str, base_asset: str, quote_asset: str, price: float, total: float):
        """ Write buy data """
        db = sqlite3.connect(r"binance_bot.sqlite")
        try:
            cursor = db.cursor()
            sqlite_insert_with_param = """INSERT INTO 'buy_history'
                                      ('pair', 'base_asset', 'quote_asset', 'price', 'total', 'date') 
                                      VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (pair, base_asset, quote_asset, price, total, datetime.now())

            cursor.execute(sqlite_insert_with_param, data_tuple)
            db.commit()

            self.update_sell_state(1)

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

    def update_sell_state(self, state: int = 0):
        db = sqlite3.connect(r"binance_bot.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute('''UPDATE state SET sell_active = ?''', (state,))
            db.commit()

        except sqlite3.Error as e:
            print(e)

    def update_buy_barrier(self, buy_barrier: float = 0):
        db = sqlite3.connect(r"binance_bot.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute('''UPDATE state SET buy_barrier = ?''', (buy_barrier,))
            db.commit()

        except sqlite3.Error as e:
            print(e)

    def read_all_orders(self, base_asset=None):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        unsorted_orders = []
        try:
            cursor = db.cursor()
            if base_asset:
                select_query = """SELECT * FROM buy_history WHERE base_asset = ? ORDER BY id ASC"""
                cursor.execute(select_query, (base_asset,))
            else:
                cursor.execute("SELECT * FROM buy_history ORDER BY id ASC")

            buy_orders_result = cursor.fetchall()

            if buy_orders_result:
                for order in buy_orders_result:
                    datetime_object = datetime.strptime(order[6], '%Y-%m-%d %H:%M:%S.%f')
                    epoch_time = int(datetime_object.timestamp())
                    entry = {'action': 'buy', 'pair': order[1], 'base_asset': order[2], 'quote_asset': order[3],
                             'price': order[4], 'total': order[5], 'date': epoch_time}
                    unsorted_orders.append(entry)

            if base_asset:
                select_query = """SELECT * FROM sell_history WHERE base_asset = ? ORDER BY id ASC"""
                cursor.execute(select_query, (base_asset,))
            else:
                cursor.execute("SELECT * FROM sell_history ORDER BY id ASC")
            sell_orders_result = cursor.fetchall()

            if sell_orders_result:
                for order in sell_orders_result:
                    datetime_object = datetime.strptime(order[6], '%Y-%m-%d %H:%M:%S.%f')
                    epoch_time = int(datetime_object.timestamp())

                    entry = {'action': 'sell', 'pair': order[1], 'base_asset': order[2], 'quote_asset': order[3],
                             'price': order[4], 'total': order[5], 'date': epoch_time}
                    unsorted_orders.append(entry)

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

        if len(unsorted_orders) > 0:
            sorted_orders = sorted(unsorted_orders, key=lambda i: i['date'], reverse=True)
            orders = []
            for order in sorted_orders:
                entry = {'action': order['action'], 'pair': order['pair'], 'base_asset': order['base_asset'],
                         'quote_asset': order['quote_asset'], 'price': order['price'], 'total': order['total'],
                         'date': datetime.fromtimestamp(order['date']).strftime("%Y-%m-%d %H:%M:%S")}
                orders.append(entry)

            return orders

    def read_last_sell_order_price(self):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        last_sell_price = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM sell_history ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()

            if result:
                last_sell_price = result[4]

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

        return last_sell_price

    def read_last_buy_order_price(self):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        last_buy_price = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM buy_history ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()

            if result:
                last_buy_price = result[4]

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

        return last_buy_price

    def read_config(self):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        config_data = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM config LIMIT 1")
            result = cursor.fetchone()

            if result:
                config_data = result

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

        return config_data

    def write_config(self, pair, base_asset, quote_asset, change_limit, minimum_profit, take_profit, max_price,
                     redcandle_size, timer, buy_trigger, sell_trigger, testmode, binance_apikey, binance_apikey_secret,
                     telegram_active, telegram_apikey, telegram_channel_id):
        """ Write buy data """
        db = sqlite3.connect(r"binance_bot.sqlite")
        try:
            cursor = db.cursor()
            cursor.execute('''UPDATE config SET pair = ?''', (pair,))
            cursor.execute('''UPDATE config SET base_asset = ?''', (base_asset,))
            cursor.execute('''UPDATE config SET quote_asset = ?''', (quote_asset,))
            cursor.execute('''UPDATE config SET change_limit = ?''', (change_limit,))
            cursor.execute('''UPDATE config SET minimum_profit = ?''', (minimum_profit,))
            cursor.execute('''UPDATE config SET take_profit = ?''', (take_profit,))
            cursor.execute('''UPDATE config SET max_price = ?''', (max_price,))
            cursor.execute('''UPDATE config SET redcandle_size = ?''', (redcandle_size,))
            cursor.execute('''UPDATE config SET timer = ?''', (timer,))
            cursor.execute('''UPDATE config SET buy_trigger = ?''', (buy_trigger,))
            cursor.execute('''UPDATE config SET sell_trigger = ?''', (sell_trigger,))
            if not testmode:
                testmode = 'off'
            cursor.execute('''UPDATE config SET testmode = ?''', (testmode,))
            cursor.execute('''UPDATE config SET binance_apikey = ?''', (binance_apikey,))
            cursor.execute('''UPDATE config SET binance_apikey_secret = ?''', (binance_apikey_secret,))
            if not telegram_active:
                telegram_active = 'off'
            cursor.execute('''UPDATE config SET telegram_active = ?''', (telegram_active,))
            cursor.execute('''UPDATE config SET telegram_apikey = ?''', (telegram_apikey,))
            cursor.execute('''UPDATE config SET telegram_channel_id = ?''', (telegram_channel_id,))

            db.commit()

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

    def read_buy_barrier(self):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        buy_barrier = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT buy_barrier FROM state LIMIT 1")
            result = cursor.fetchone()

            if result:
                buy_barrier = float(result[0])

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

        if type(buy_barrier) == float:
            return buy_barrier

    def is_selling(self):
        """ create a database connection to a SQLite database """
        db = sqlite3.connect(r"binance_bot.sqlite")
        sell_state = None
        try:
            cursor = db.cursor()
            cursor.execute("SELECT sell_active FROM state LIMIT 1")
            result = cursor.fetchone()

            if result:
                sell_state = result[0]

        except sqlite3.Error as e:
            print(e)
        finally:
            db.close()

        if sell_state == 1:
            return sell_state
