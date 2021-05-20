%include('header.tpl', title='Graph')
<div class="content">
<div class="headlineSeperator"> <h2> Graph </h2> </div>

<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
    <div id="tradingview_fca88"></div>
    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/{{pair}}/?exchange=BINANCE" rel="noopener" target="_blank"><span class="blue-text">{{pair}} Chart</span></a> by TradingView</div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
        new TradingView.widget(
            {
                "width": 1500,
                "height": 610,
                "symbol": "BINANCE:{{pair}}",
                "interval": "1",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#f1f3f6",
                "enable_publishing": false,
                "allow_symbol_change": true,
                "details": true,
                "studies": [
                    "MOM@tv-basicstudies",
                    "MF@tv-basicstudies",
                    "MASimple@tv-basicstudies",
                    "RSI@tv-basicstudies"
                ],
                "container_id": "tradingview_fca88"
            }
        );
    </script>
</div>
<!-- TradingView Widget END -->

</div>

</div>
%include('footer.tpl')