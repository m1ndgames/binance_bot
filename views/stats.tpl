%include('header.tpl', title='Stats')

%if orders:
    %for order in orders:
        {{order['action']}} - {{order['pair']}} - {{order['base_asset']}} - {{order['quote_asset']}} - {{order['price']}} - {{order['total']}} - {{order['date']}}<br>
    %end
%end

%include('footer.tpl')