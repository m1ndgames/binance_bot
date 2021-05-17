%include('header.tpl', title='Graph')
<div class="content">
<div class="headlineSeperator"> <h2> Graph </h2> </div>

<div class="tradingview-widget-container">
    <div id="tradingview_7d799"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>

    <script type="text/javascript">
        new TradingView.widget({
            "autosize": true,
            "symbol": "BINANCE:{{pair}}",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "0",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": true,
            "range": "5D",
            "save_image": false,
            "details": true,
            "container_id": "tradingview_7d799"
        });
    </script>
</div>

</div>
%include('footer.tpl')