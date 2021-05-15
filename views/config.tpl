%include('header.tpl', title='Config')

  <script>
  $( function() {
    $( "#show-option" ).tooltip({
      show: {
        effect: "slideDown",
        delay: 250
      }
    });
    $( "#hide-option" ).tooltip({
      hide: {
        effect: "explode",
        delay: 250
      }
    });
    $( "#open-event" ).tooltip({
      show: null,
      position: {
        my: "left top",
        at: "left bottom"
      },
      open: function( event, ui ) {
        ui.tooltip.animate({ top: ui.tooltip.position().top + 10 }, "fast" );
      }
    });
  } );
  </script>

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
        <input type="text" id="pair" name="pair" value="{{pair}}" title="The trading pair, for example BTCUSDT."><br>
    %else:
        <input type="text" id="pair" name="pair" title="The trading pair, for example BTCUSDT."><br>
    %end
    </div>

<div class="grid-item">
    <label for="base_asset">Base Asset:</label><br>
    %if base_asset:
        <input type="text" id="base_asset" name="base_asset" value="{{base_asset}}" title="Base asset name, for example BTC."><br>
    %else:
        <input type="text" id="base_asset" name="base_asset" title="Test" title="Base asset name, for example BTC."><br>
    %end
    </div>
<div class="grid-item">
    <label for="quote_asset">Quote Asset:</label><br>
    %if quote_asset:
        <input type="text" id="quote_asset" name="quote_asset" value="{{quote_asset}}" title="Quote asset name, for example USDT."><br>
    %else:
        <input type="text" id="quote_asset" name="quote_asset" title="Quote asset name, for example USDT."><br>
    %end
    </div>

<div class="grid-item">
    <label for="change_limit">Change limit:</label><br>
    %if change_limit:
        <input type="text" id="change_limit" name="change_limit" value="{{change_limit}}" title="This defines the change in price that the bot checks against each timer loop, when the change is higher than this value, the counter is raised."><br>
    %else:
        <input type="text" id="change_limit" name="change_limit" title="This defines the change in price that the bot checks against each timer loop, when the change is higher than this value, the counter is raised."><br>
    %end
    </div>
<div class="grid-item">

    <label for="minimum_profit">Minimum profit:</label><br>
    %if minimum_profit:
        <input type="text" id="minimum_profit" name="minimum_profit" value="{{minimum_profit}}" title="When buy price + this value is reached the bot sells. (When the sell counter requirement is fulfilled)"><br>
    %else:
        <input type="text" id="minimum_profit" name="minimum_profit" title="When buy price + this value is reached the bot sells. (When the sell counter requirement is fulfilled)"><br>
    %end
    </div>
<div class="grid-item">
    <label for="take_profit">Take profit:</label><br>
    %if take_profit:
        <input type="text" id="take_profit" name="take_profit" value="{{take_profit}}" title="When buy price + this value is reached, the bot sells without checking the sell counter."><br>
    %else:
        <input type="text" id="take_profit" name="take_profit" title="When buy price + this value is reached, the bot sells without checking the sell counter."><br>
    %end
    </div>
<div class="grid-item">
    <label for="max_price">Maximum price:</label><br>
    %if max_price:
        <input type="text" id="max_price" name="max_price" value="{{max_price}}" title="The bot won't buy above this price."><br>
    %else:
        <input type="text" id="max_price" name="max_price" title="The bot won't buy above this price."><br>
    %end
    </div>
<div class="grid-item">
    <label for="redcandle_size">Red candle size:</label><br>
    %if redcandle_size:
        <input type="text" id="redcandle_size" name="redcandle_size" value="{{redcandle_size}}" title="The bot will save the last sell price and subtract this value. This is the new buy barrier and the bot will not buy until the price drops below it."><br>
    %else:
        <input type="text" id="redcandle_size" name="redcandle_size" title="The bot will save the last sell price and subtract this value. This is the new buy barrier and the bot will not buy until the price drops below it."><br>
    %end
    </div>
<div class="grid-item">
    <label for="timer">Timer:</label><br>
    %if timer:
        <input type="text" id="timer" name="timer" value="{{timer}}" title="The timer loop in seconds. When it reaches 0 the bot checks for changes."><br>
    %else:
        <input type="text" id="timer" name="timer" title="The timer loop in seconds. When it reaches 0 the bot checks for changes."><br>
    %end
    </div>
<div class="grid-item">
    <label for="buy_trigger">Buy trigger count:</label><br>
    %if buy_trigger:
        <input type="text" id="buy_trigger" name="buy_trigger" value="{{buy_trigger}}" title="This defines how often the change limit must have been reached. If the counter reaches the value and all other requirements are met, it buys."><br>
    %else:
        <input type="text" id="buy_trigger" name="buy_trigger" title="This defines how often the change limit must have been reached. If the counter reaches the value and all other requirements are met, it buys."><br>
    %end
    </div>
<div class="grid-item">
    <label for="sell_trigger">Sell trigger count:</label><br>
    %if sell_trigger:
        <input type="text" id="sell_trigger" name="sell_trigger" value="{{sell_trigger}}" title="This defines how often the change limit must have been reached. If the counter reaches the value and all other requirements are met, it sells."><br>
    %else:
        <input type="text" id="sell_trigger" name="sell_trigger" title="This defines how often the change limit must have been reached. If the counter reaches the value and all other requirements are met, it sells."><br>
    %end
    </div>
<div class="grid-item">
    <label for="testmode">Test Mode:</label><br>
    %if testmode == 'on':
        <input type="checkbox" id="testmode" name="testmode" value="on" title="If this is active no orders are processed." checked><br>
    %else:
        <input type="checkbox" id="testmode" name="testmode" value="on" title="If this is active no orders are processed."><br>
    %end
    </div>
%if buy_barrier:
<div class="grid-item">
    <label for="buy_barrier">Buy Barrier:</label><br>
        <input type="text" id="buy_barrier" name="buy_barrier" value="{{buy_barrier}}" title="The bot will not buy above this barrier. It's set according to the last sell price minus the red candle size."><br>
    </div>
%end
<div class="grid-item">
    <label for="buy_barrier_step_size">Buy Barrier step size:</label><br>
    <input type="text" id="buy_barrier_step_size" name="buy_barrier_step_size" value="{{buy_barrier_step_size}}" title="This defines the size of each step the buy barrier is raised, if activated."><br>
    </div>
<div class="grid-item">
    <label for="buy_barrier_timer">Buy Barrier Timer:</label><br>
    <input type="text" id="buy_barrier_timer" name="buy_barrier_timer" value="{{buy_barrier_timer}}" title="This defines the timer (in seconds) after the buy barrier is raised, if activated."><br>
    </div>
<div class="grid-item">
    <label for="buy_barrier_timer_enabled">Buy Barrier Timer Active:</label><br>
    %if buy_barrier_timer_enabled == 'on':
        <input type="checkbox" id="buy_barrier_timer_enabled" name="buy_barrier_timer_enabled" value="on" title="If active, the bot will raise the buy barrier automatically when the buy barrier timer is reached till it reaches the defined max buy price." checked><br>
    %else:
        <input type="checkbox" id="buy_barrier_timer_enabled" name="buy_barrier_timer_enabled" value="on" title="If active, the bot will raise the buy barrier automatically when the buy barrier timer is reached till it reaches the defined max buy price."><br>
    %end
    </div></div>
    <div class="grid-container">
   <div class="formSeperator"> <h2>Binance API Settings</h2> </div> </div>
   <div class="grid-container-api">

<div class="grid-item-api">
    <label for="binance_apikey">API key:</label><br>
    %if binance_apikey:
        <input type="text" id="binance_apikey" name="binance_apikey" value="{{binance_apikey}}" title="The Binance API key"><br>
    %else:
        <input type="text" id="binance_apikey" name="binance_apikey" title="The Binance API key"><br>
    %end
    </div>
<div class="grid-item-api">
    <label for="binance_apikey_secret">API key secret:</label><br>
    %if binance_apikey_secret:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret" value="{{binance_apikey_secret}}" title="The Binance API key secret"><br>
    %else:
        <input type="text" id="binance_apikey_secret" name="binance_apikey_secret" title="The Binance API key secret"><br>
    %end
    </div>

    </div>
    <div class="grid-container">
   <div class="formSeperator"> <h2>Telegram Settings</h2></div></div>
   <div class="grid-container-tele">

<div class="grid-item-tele">
    <label for="telegram_active">Active:</label><br>
    %if telegram_active == 'on':
        <input type="checkbox" id="telegram_active" name="telegram_active" value="on" title="When active, the bot will notify you via Telegram about buy/sell actions and crashes." checked><br>
    %else:
        <input type="checkbox" id="telegram_active" name="telegram_active" value="on" title="When active, the bot will notify you via Telegram about buy/sell actions and crashes."><br>
    %end
    </div>
<div class="grid-item-tele">
    <label for="telegram_apikey">API key:</label><br>
    %if telegram_apikey:
        <input type="text" id="telegram_apikey" name="telegram_apikey" value="{{telegram_apikey}}" title="The Telegram API key."><br>
    %else:
        <input type="text" id="telegram_apikey" name="telegram_apikey" title="The Telegram API key."><br>
    %end
    </div>
<div class="grid-item-tele">
    <label for="telegram_channel_id">Channel ID:</label><br>
    %if telegram_channel_id:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id" value="{{telegram_channel_id}}" title="The Telegram channel ID."><br>
    %else:
        <input type="text" id="telegram_channel_id" name="telegram_channel_id" title="The Telegram channel ID."><br>
    %end
</div>
</div>
    <input type="submit" value="Save">
</form>
</div>

%include('footer.tpl')