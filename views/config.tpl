%include('header.tpl', title='Config')
<div class="formWrapper ">
<form method="post" action="saveconfig">
<div class="grid-container">
<div class="formSeperator"><h2>Trade Settings</h2></div>
<div class="grid-item"></div>
<div class="grid-item"></div>
<div class="grid-item"></div>
<div class="grid-item"
    <label for="pair">Trading Pair:</label><br>
    %if buy_trigger:
        <input type="text" id="pair" name="pair" value="{{pair}}"><br>
    %else:
        <input type="text" id="pair" name="pair"><br>
    %end
    </div>

<div class="grid-item">
    <label for="base_asset">Base Asset:</label><br>
    %if base_asset:
        <input type="text" id="base_asset" name="base_asset" value="{{base_asset}}"><br>
    %else:
        <input type="text" id="base_asset" name="base_asset"><br>
    %end
    </div>
<div class="grid-item">
    <label for="quote_asset">Quote Asset:</label><br>
    %if quote_asset:
        <input type="text" id="quote_asset" name="quote_asset" value="{{quote_asset}}"><br>
    %else:
        <input type="text" id="quote_asset" name="quote_asset"><br>
    %end
    </div>

<div class="grid-item">
    <label for="change_limit">Change limit:</label><br>
    %if change_limit:
        <input type="text" id="change_limit" name="change_limit" value="{{change_limit}}"><br>
    %else:
        <input type="text" id="change_limit" name="change_limit"><br>
    %end
    </div>
<div class="grid-item">

    <label for="minimum_profit">Minimum profit:</label><br>
    %if minimum_profit:
        <input type="text" id="minimum_profit" name="minimum_profit" value="{{minimum_profit}}"><br>
    %else:
        <input type="text" id="minimum_profit" name="minimum_profit"><br>
    %end
    </div>
<div class="grid-item">
    <label for="take_profit">Take profit:</label><br>
    %if take_profit:
        <input type="text" id="take_profit" name="take_profit" value="{{take_profit}}"><br>
    %else:
        <input type="text" id="take_profit" name="take_profit"><br>
    %end
    </div>
<div class="grid-item">
    <label for="max_price">Maximum price:</label><br>
    %if max_price:
        <input type="text" id="max_price" name="max_price" value="{{max_price}}"><br>
    %else:
        <input type="text" id="max_price" name="max_price"><br>
    %end
    </div>
<div class="grid-item">
    <label for="redcandle_size">Red candle size:</label><br>
    %if redcandle_size:
        <input type="text" id="redcandle_size" name="redcandle_size" value="{{redcandle_size}}"><br>
    %else:
        <input type="text" id="redcandle_size" name="redcandle_size"><br>
    %end
    </div>
<div class="grid-item">
    <label for="timer">Timer:</label><br>
    %if timer:
        <input type="text" id="timer" name="timer" value="{{timer}}"><br>
    %else:
        <input type="text" id="timer" name="timer"><br>
    %end
    </div>
<div class="grid-item">
    <label for="buy_trigger">Buy trigger count:</label><br>
    %if buy_trigger:
        <input type="text" id="buy_trigger" name="buy_trigger" value="{{buy_trigger}}"><br>
    %else:
        <input type="text" id="buy_trigger" name="buy_trigger"><br>
    %end
    </div>
<div class="grid-item">
    <label for="sell_trigger">Sell trigger count:</label><br>
    %if sell_trigger:
        <input type="text" id="sell_trigger" name="sell_trigger" value="{{sell_trigger}}"><br>
    %else:
        <input type="text" id="sell_trigger" name="sell_trigger"><br>
    %end
    </div>
<div class="grid-item">
    <label for="testmode">Test Mode:</label><br>
    %if testmode == 'on':
        <input type="checkbox" id="testmode" name="testmode" value="on" checked><br>
    %else:
        <input type="checkbox" id="testmode" name="testmode" value="on"><br>
    %end
    </div>
%if buy_barrier:
<div class="grid-item">
    <label for="buy_barrier">Buy Barrier:</label><br>
        <input type="text" id="buy_barrier" name="buy_barrier" value="{{buy_barrier}}"><br>
    </div>
%end
<div class="grid-item">
    <label for="buy_barrier_step_size">Buy Barrier step size:</label><br>
    <input type="text" id="buy_barrier_step_size" name="buy_barrier_step_size" value="{{buy_barrier_step_size}}"><br>
    </div>
<div class="grid-item">
    <label for="buy_barrier_timer">Buy Barrier Timer:</label><br>
    <input type="text" id="buy_barrier_timer" name="buy_barrier_timer" value="{{buy_barrier_timer}}"><br>
    </div>
<div class="grid-item">
    <label for="buy_barrier_timer_enabled">Buy Barrier Timer Active:</label><br>
    %if buy_barrier_timer_enabled == 'on':
        <input type="checkbox" id="buy_barrier_timer_enabled" name="buy_barrier_timer_enabled" value="on" checked><br>
    %else:
        <input type="checkbox" id="buy_barrier_timer_enabled" name="buy_barrier_timer_enabled" value="on"><br>
    %end
    </div></div>
    <div class="grid-container">
   <div class="formSeperator"> <h2>Binance API Settings</h2> </div> </div>
   <div class="grid-container-api">

<div class="grid-item-api">
    <label for="binance_apikey">API key:</label><br>
    %if binance_apikey:
        <input type="text" id="binance_apikey" name="binance_apikey" value="{{binance_apikey}}"><br>
    %else:
        <input type="text" id="binance_apikey" name="binance_apikey"><br>
    %end
    </div>
<div class="grid-item-api">
    <label for="binance_apikey_secret">API key secret:</label><br>
    %if binance_apikey_secret:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret" value="{{binance_apikey_secret}}"><br>
    %else:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret"><br>
    %end
    </div>

    </div>
    <div class="grid-container">
   <div class="formSeperator"> <h2>Telegram Settings</h2></div></div>
   <div class="grid-container-tele">

<div class="grid-item-tele">
    <label for="telegram_active">Active:</label><br>
    %if telegram_active == 'on':
        <input type="checkbox" id="telegram_active" name="telegram_active" value="on" checked><br>
    %else:
        <input type="checkbox" id="telegram_active" name="telegram_active" value="on"><br>
    %end
    </div>
<div class="grid-item-tele">
    <label for="telegram_apikey">API key:</label><br>
    %if telegram_apikey:
        <input type="text" id="telegram_apikey" name="telegram_apikey" value="{{telegram_apikey}}"><br>
    %else:
        <input type="text" id="telegram_apikey" name="telegram_apikey"><br>
    %end
    </div>
<div class="grid-item-tele">
    <label for="telegram_channel_id">Channel ID:</label><br>
    %if telegram_channel_id:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id" value="{{telegram_channel_id}}"><br>
    %else:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id"><br>
    %end
</div>
</div>
    <input type="submit" value="Save">
</form>
</div>

%include('footer.tpl')