%include('header.tpl', title='Config')

<form method="post" action="saveconfig">
    <label for="pair">Trading Pair:</label><br>
    %if buy_trigger:
        <input type="text" id="pair" name="pair" value="{{pair}}"><br>
    %else:
        <input type="text" id="pair" name="pair"><br>
    %end

    <label for="base_asset">Base Asset:</label><br>
    %if base_asset:
        <input type="text" id="base_asset" name="base_asset" value="{{base_asset}}"><br>
    %else:
        <input type="text" id="base_asset" name="base_asset"><br>
    %end

    <label for="quote_asset">Quote Asset:</label><br>
    %if quote_asset:
        <input type="text" id="quote_asset" name="quote_asset" value="{{quote_asset}}"><br>
    %else:
        <input type="text" id="quote_asset" name="quote_asset"><br>
    %end

    <label for="change_limit">Change limit:</label><br>
    %if change_limit:
        <input type="text" id="change_limit" name="change_limit" value="{{change_limit}}"><br>
    %else:
        <input type="text" id="change_limit" name="change_limit"><br>
    %end

    <label for="minimum_profit">Minimum profit:</label><br>
    %if minimum_profit:
        <input type="text" id="minimum_profit" name="minimum_profit" value="{{minimum_profit}}"><br>
    %else:
        <input type="text" id="minimum_profit" name="minimum_profit"><br>
    %end

    <label for="take_profit">Take profit:</label><br>
    %if take_profit:
        <input type="text" id="take_profit" name="take_profit" value="{{take_profit}}"><br>
    %else:
        <input type="text" id="take_profit" name="take_profit"><br>
    %end

    <label for="max_price">Maximum price:</label><br>
    %if max_price:
        <input type="text" id="max_price" name="max_price" value="{{max_price}}"><br>
    %else:
        <input type="text" id="max_price" name="max_price"><br>
    %end

    <label for="redcandle_size">Red candle size:</label><br>
    %if redcandle_size:
        <input type="text" id="redcandle_size" name="redcandle_size" value="{{redcandle_size}}"><br>
    %else:
        <input type="text" id="redcandle_size" name="redcandle_size"><br>
    %end

    <label for="timer">Timer:</label><br>
    %if timer:
        <input type="text" id="timer" name="timer" value="{{timer}}"><br>
    %else:
        <input type="text" id="timer" name="timer"><br>
    %end

    <label for="buy_trigger">Buy trigger count:</label><br>
    %if buy_trigger:
        <input type="text" id="buy_trigger" name="buy_trigger" value="{{buy_trigger}}"><br>
    %else:
        <input type="text" id="buy_trigger" name="buy_trigger"><br>
    %end

    <label for="sell_trigger">Sell trigger count:</label><br>
    %if sell_trigger:
        <input type="text" id="sell_trigger" name="sell_trigger" value="{{sell_trigger}}"><br>
    %else:
        <input type="text" id="sell_trigger" name="sell_trigger"><br>
    %end

    <label for="testmode">Test Mode:</label><br>
    %if testmode == 'on':
        <input type="checkbox" id="testmode" name="testmode" value="on" checked><br>
    %else:
        <input type="checkbox" id="testmode" name="testmode" value="on"><br>
    %end

    <label for="binance_apikey">Binance API key:</label><br>
    %if binance_apikey:
        <input type="text" id="binance_apikey" name="binance_apikey" value="{{binance_apikey}}"><br>
    %else:
        <input type="text" id="binance_apikey" name="binance_apikey"><br>
    %end

    <label for="binance_apikey_secret">Binance API key secret:</label><br>
    %if binance_apikey_secret:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret" value="{{binance_apikey_secret}}"><br>
    %else:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret"><br>
    %end

    <label for="telegram_active">Telegram Bot:</label><br>
    %if telegram_active == 'on':
        <input type="checkbox" id="telegram_active" name="telegram_active" value="on" checked><br>
    %else:
        <input type="checkbox" id="telegram_active" name="telegram_active" value="on"><br>
    %end

    <label for="telegram_apikey">Telegram API key:</label><br>
    %if telegram_apikey:
        <input type="text" id="telegram_apikey" name="telegram_apikey" value="{{telegram_apikey}}"><br>
    %else:
        <input type="text" id="telegram_apikey" name="telegram_apikey"><br>
    %end

    <label for="telegram_channel_id">Telegram channel ID:</label><br>
    %if telegram_channel_id:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id" value="{{telegram_channel_id}}"><br>
    %else:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id"><br>
    %end

    <input type="submit" value="Submit">
</form>


%include('footer.tpl')