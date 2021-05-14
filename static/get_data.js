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
        $('#base_asset_buy_price').html(
            data.base_asset_buy_price
        );
        $('#base_asset_sell_price').html(
            data.base_asset_sell_price
        );
        $('#base_asset_take_profit_price').html(
            data.base_asset_take_profit_price
        );
        $('#sell_counter').html(
            data.sell_counter
        );
        $('#sell_trigger').html(
            data.sell_trigger
        );
        $('#buy_counter').html(
            data.buy_counter
        );
        $('#buy_trigger').html(
            data.buy_trigger
        );
        $('#base_asset_change').html(
            data.base_asset_change
        );
    });
}

setInterval(loadData, 1000);