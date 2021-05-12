%include('header.tpl', title='Config')

<form method="post" action="saveconfig">
    <label for="pair">Trading Pair:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="pair" name="pair" value="{{config['pair']}}"><br>
    %else:
        <input type="text" id="pair" name="pair"><br>

    <label for="base_asset">Base Asset:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="base_asset" name="base_asset" value="{{config['base_asset']}}"><br>
    %else:
        <input type="text" id="base_asset" name="base_asset"><br>

    <label for="quote_asset">Quote Asset:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="quote_asset" name="quote_asset" value="{{config['quote_asset']}}"><br>
    %else:
        <input type="text" id="quote_asset" name="quote_asset"><br>

    <label for="change_limit">Change limit:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="change_limit" name="change_limit" value="{{config['change_limit']}}"><br>
    %else:
        <input type="text" id="change_limit" name="change_limit"><br>

    <label for="minimum_profit">Minimum profit:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="minimum_profit" name="minimum_profit" value="{{config['minimum_profit']}}"><br>
    %else:
        <input type="text" id="minimum_profit" name="minimum_profit"><br>

    <label for="take_profit">Take profit:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="take_profit" name="take_profit" value="{{config['take_profit']}}"><br>
    %else:
        <input type="text" id="take_profit" name="take_profit"><br>

    <label for="max_price">Maximum price:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="max_price" name="max_price" value="{{config['max_price']}}"><br>
    %else:
        <input type="text" id="max_price" name="max_price"><br>

    <label for="redcandle_size">Red candle size:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="redcandle_size" name="redcandle_size" value="{{config['redcandle_size']}}"><br>
    %else:
        <input type="text" id="redcandle_size" name="redcandle_size"><br>

    <label for="timer">Timer:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="timer" name="timer" value="{{config['timer']}}"><br>
    %else:
        <input type="text" id="timer" name="timer"><br>

    <label for="buy_trigger">Buy trigger count:</label><br>
    %if config['buy_trigger']:
        <input type="text" id="buy_trigger" name="buy_trigger" value="{{config['buy_trigger']}}"><br>
    %else:
        <input type="text" id="buy_trigger" name="buy_trigger"><br>

    <label for="sell_trigger">Sell trigger count:</label><br>
    %if config['sell_trigger']:
        <input type="text" id="sell_trigger" name="sell_trigger" value="{{config['sell_trigger']}}"><br>
    %else:
        <input type="text" id="sell_trigger" name="sell_trigger"><br>

    <label for="testmode">Test Mode:</label><br>
    %if config['testmode'] == 1:
        <input type="text" id="testmode" name="testmode" value="1" checked><br>
    %else:
        <input type="text" id="testmode" name="testmode"><br>

    <label for="binance_apikey">Binance API key:</label><br>
    %if config['binance_apikey']:
        <input type="text" id="binance_apikey" name="binance_apikey" value="{{config['binance_apikey']}}"><br>
    %else:
        <input type="text" id="binance_apikey" name="binance_apikey"><br>

    <label for="binance_apikey_secret">Binance API key secret:</label><br>
    %if config['binance_apikey_secret']:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret" value="{{config['binance_apikey_secret']}}"><br>
    %else:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret"><br>

    <label for="telegram_active">Telegram Bot:</label><br>
    %if config['telegram_active'] == 1:
        <input type="checkbox" id="telegram_active" name="telegram_active" value="1" checked><br>
    %else:
        <input type="checkbox" id="telegram_active" name="telegram_active" value="0"><br>

    <label for="telegram_apikey">Telegram API key:</label><br>
    %if config['telegram_apikey']:
        <input type="text" id="telegram_apikey" name="telegram_apikey" value="{{config['telegram_apikey']}}"><br>
    %else:
        <input type="text" id="telegram_apikey" name="telegram_apikey"><br>

    <label for="telegram_channel_id">Telegram channel ID:</label><br>
    %if config['telegram_channel_id']:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id" value="{{config['telegram_channel_id']}}"><br>
    %else:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id"><br>

    <input type="submit" value="Submit">
</form>


%include('footer.tpl')