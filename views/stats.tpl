%include('header.tpl', title='Stats')
<div class="content">
<div class="headlineSeperator"> <h2> Stats </h2> </div>

%if orders:
<script type="application/javascript" src="/static/tablefilter/tablefilter.js"></script>

<table id="statsTable" style="width:100%">
    <thead style="width:100%">
        <tr class="sorter-false">
            <td>Action</td>
            <td>Trading Pair</td>
            <td>Base Asset</td>
            <td>Quote Asset</td>
            <td>Price</td>
            <td>Total</td>
            <td>Date</td>
        </tr>
    </thead>

    %for order in orders:
    <tr>
        <td>
            {{order['action']}}
        </td>
        <td>
            {{order['pair']}}
        </td>
        <td>
            {{order['base_asset']}}
        </td>
        <td>
            {{order['quote_asset']}}
        </td>
        <td>
            {{order['price']}}
        </td>
        <td>
            {{order['total']}}
        </td>
        <td>
            {{order['date']}}
        </td>
    %end
    </tr>
</table>

<script>
    var filtersConfig = {
        base_path: '/static/tablefilter/',

        auto_filter: {
            delay: 1100
        },

        paging: {
          results_per_page: ['Records: ', [25, 50, 100, 250]]
        },

        state: {
            types: ['local_storage'],
            filters: true,
            page_number: true,
            page_length: true,
            sort: false
        },

        sticky_headers: true,
        filters_row_index: 1,
        loader: true,
        state: true,
        dataSorter: false,

        grid_layout: {
            width: '100%',
            filters: true,
            cont_css_class: 'grd-main-cont',
            tbl_head_css_class: 'grd-head-cont',
            tbl_cont_css_class: 'grd-cont'
        },

        alternate_rows: true,
        rows_counter: false,
        btn_reset: false,
        status_bar: false,
        toolbar: true,
        mark_active_columns: true,
        highlight_keywords: true,
        msg_filter: 'Filtering...',
        loader: {
            html: '<div id="lblMsg"></div>',
            css_class: 'myLoader'
        },
        status_bar: {
            target_id: 'lblMsg',
            css_class: 'myStatus'
        },
        col_0: 'select',
        col_1: 'select',
        col_2: 'select',
        col_3: 'select',
        col_widths: [
            "10%", "12%", "10%",
            "10%", "12%", "12%",
            "20%"
        ],
        col_types: [
            'string', 'string', 'string',
            'string', 'number', 'number',
            'string'
        ],
        extensions:[{
            name: 'sort'
        }]
    };

    var tf = new TableFilter('statsTable', filtersConfig);
    tf.init();
</script>
%end

</div>
%include('footer.tpl')