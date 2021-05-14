%include('header.tpl', title='Stats')
<div class="content">
<div class="headlineSeperator"> <h2> Stats </h2> </div>
%if orders:
    %for order in orders:
        {{order['action']}} - {{order['pair']}} - {{order['base_asset']}} - {{order['quote_asset']}} - {{order['price']}} - {{order['total']}} - {{order['date']}}<br>
    %end
%end
</div>
%include('footer.tpl')