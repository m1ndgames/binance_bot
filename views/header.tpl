<!DOCTYPE html>
<html>
<head>
<title>Binance Bot - {{title}}</title>
<meta charset="UTF-8">

<script src="https://code.jquery.com/jquery-1.11.3.js"></script>
<script src="/static/get_data.js"></script>

</head>
<body>

<a href="/">Index</a> - <a href="/config">Config</a> - <a href="/stats">Stats</a>
<br><br>

Countdown Timer: <div id='countdown_timer'></div><br>
Pair: <div id='trading_pair'></div><br><br>
Price: <div id='price'></div><br>
Buy Barrier: <div id='buy_barrier'></div><br>
<br>
Balance:<br>
<div id='base_asset_balance'></div>
<div id='quote_asset_balance'></div>
<br>
Buy Price: <div id='base_asset_buy_price'></div>
Sell Price: <div id='base_asset_sell_price'></div>
Take Profit: <div id='base_asset_take_profit_price'></div>
Sell Counter: <div id='sell_counter'></div>
Sell Trigger: <div id='sell_trigger'></div>
Buy Counter: <div id='buy_counter'></div>
Buy Trigger: <div id='buy_trigger'></div>
Base Asset change: <div id='base_asset_change'></div>
<br>