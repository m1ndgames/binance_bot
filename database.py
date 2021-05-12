import datetime
import sqlite3

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


def setup_database():
    """ create a database connection to a SQLite database """
    db = sqlite3.connect(r"binance_bot.sqlite")
    try:
        print("Connected to sqlite db v." + str(sqlite3.version))
        create_table(db, sql_buy_table)
        create_table(db, sql_sell_table)
        create_table(db, sql_state_table)

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

    except sqlite3.Error as e:
        print(e)
    finally:
        db.close()


def create_table(conn, create_table_sql):
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


def write_sell_data(pair: str, base_asset: str, quote_asset: str, price: float, total: float):
    """ Write sell data """
    db = sqlite3.connect(r"binance_bot.sqlite")
    try:
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO 'sell_history'
                                  ('pair', 'base_asset', 'quote_asset', 'price', 'total', 'date') 
                                  VALUES (?, ?, ?, ?, ?, ?);"""

        data_tuple = (pair, base_asset, quote_asset, price, total, datetime.datetime.now())

        cursor.execute(sqlite_insert_with_param, data_tuple)
        db.commit()

        update_sell_state(0)
        update_buy_barrier(price - 0.10)

    except sqlite3.Error as e:
        print(e)
    finally:
        db.close()


def write_buy_data(pair: str, base_asset: str, quote_asset: str, price: float, total: float):
    """ Write buy data """
    db = sqlite3.connect(r"binance_bot.sqlite")
    try:
        cursor = db.cursor()
        sqlite_insert_with_param = """INSERT INTO 'buy_history'
                                  ('pair', 'base_asset', 'quote_asset', 'price', 'total', 'date') 
                                  VALUES (?, ?, ?, ?, ?, ?);"""

        data_tuple = (pair, base_asset, quote_asset, price, total, datetime.datetime.now())

        cursor.execute(sqlite_insert_with_param, data_tuple)
        db.commit()

        update_sell_state(1)

    except sqlite3.Error as e:
        print(e)
    finally:
        db.close()


def update_sell_state(state: int = 0):
    db = sqlite3.connect(r"binance_bot.sqlite")
    try:
        cursor = db.cursor()
        cursor.execute('''UPDATE state SET sell_active = ?''', (state,))
        db.commit()

    except sqlite3.Error as e:
        print(e)


def update_buy_barrier(buy_barrier: float = 0):
    db = sqlite3.connect(r"binance_bot.sqlite")
    try:
        cursor = db.cursor()
        cursor.execute('''UPDATE state SET buy_barrier = ?''', (buy_barrier,))
        db.commit()

    except sqlite3.Error as e:
        print(e)


def read_last_sell_order_price():
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


def read_last_buy_order_price():
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


def read_buy_barrier():
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


def is_selling():
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
