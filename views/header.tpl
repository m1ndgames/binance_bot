<!DOCTYPE html>
<html>
<head>
<title>Binance Bot - {{title}}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />
<script src="https://code.jquery.com/jquery-1.11.3.js"></script>
<script src="/static/get_data.js"></script>
<link rel="stylesheet" type="text/css" href="/static/style.css"/>
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Wallpoet&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Oxanium:wght@200;300;400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="shortcut icon" type="image/x-icon" href="../img/favicon-80x80.png">

</head>
<body>
<div class="logo">
<div class="logoContent">
<h1>Binance</h1>
 <img src="../img/binance-bot_logo.png" alt="Binance Bot"  height="200">
 <h1>Bot</h1>
</div>
</div>
<div class="navigation">
<a href="/"><span class="material-icons"> home</span> Home</a> -
<a href="/config"><span class="material-icons">settings</span> Config</a> -
<a href="/stats"><span class="material-icons">trending_up</span> Stats</a>
</div>

<div class="ticker">
<div class="tickerContent">
<div class="tickerItem"><div class="title">Timer:</div><div class="value" id='countdown_timer'></div></div>
<div class="tickerItem"><div class="title">Pair:</div> <div class="value" id='trading_pair'></div></div>
<div class="tickerItem"><div class="title">Price:</div> <div class="value" id='price'></div></div>
%if not is_selling == 1:
<div class="tickerItem"><div class="title">Buy Barrier: </div><div class="value" id='buy_barrier'></div></div>
%end
<div class="tickerItem"><div class="title">Balance:</div><div class="value" id='base_asset_balance'></div><div class="value" id='quote_asset_balance'></div></div>
</br>
</div>
<div class="seperator"></div>
<div class="tickerContent">
%if is_selling == 1:
<div class="tickerItem"><div class="title">Buy Price:</div> <div class="value" id='base_asset_buy_price'></div></div>
<div class="tickerItem"><div class="title">Sell Price:</div> <div class="value" id='base_asset_sell_price'></div></div>
<div class="tickerItem"><div class="title">Take Profit:</div> <div class="value" id='base_asset_take_profit_price'></div></div>
%end
%if is_selling == 1:
<div class="tickerItem"><div class="title">Sell Counter:</div> <div class="value" id='sell_counter'></div>
<div class="value">/</div>
<div class="value" id='sell_trigger'></div></div>
%else:
<div class="tickerItem"><div class="title">Buy Counter:</div><div class="value" id='buy_counter'></div>
<div class="value">/</div>
<div class="value" id='buy_trigger'></div></div>
%end
<div class="tickerItem"><div class="title">Base Asset change:</div> <div class="value"  id='base_asset_change'></div></div>
<br>
</div></div>