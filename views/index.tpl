%include('header.tpl', title='Index')

<script>
    $.ajaxSetup({ cache: false });

    function loadData(){
        $.getJSON("/api/asset_data",
        function(data) {
            $('#countdown_timer').html(
                data.countdown_timer
            );
            $('#trading_pair').html(
                data.pair
            );
            $('#price').html(
                data.base_asset_name + " = " + data.base_asset_price + " " + data.quote_asset_name
            );
            $('#base_asset_balance').html(
                data.base_asset_balance_precision + " " + data.base_asset_name
            );
            $('#quote_asset_balance').html(
                data.quote_asset_balance_precision + " " + data.quote_asset_name
            );
            $('#buy_barrier').html(
                data.buy_barrier
            );
        });
    }
    setInterval(loadData,{{countdown * 100}});
</script>


Countdown Timer: <div id='countdown_timer'></div><br>
Pair: <div id='trading_pair'></div><br><br>
Price: <div id='price'></div><br>
Buy Barrier: <div id='buy_barrier'></div><br>
<br>
Balance:<br>
<div id='base_asset_balance'></div>
<div id='quote_asset_balance'></div>

%include('footer.tpl', version='0.1')
