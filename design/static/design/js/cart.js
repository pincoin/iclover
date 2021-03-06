var $cart_body = $('#cart_body');
    function cartList(data){
        var new_json = JSON.parse(data['json_text']);
        $cart_body.append(
            '<div class="list-group-item flex-column justify-content-between align-items-center">' +
            '<button type="button" class="close text-danger cart_delete_btn" data-dismiss="modal"' +
            'aria-label="Close" name="' + data['uuid'] + '" onclick="cart_delete($(this));"><span aria-hidden="true">×</span></button>' +
            '<span class="text-black-50" style="font-size:12px;">' +
            new_json.title + '<br>' + ' ' + new_json.size_text + ' ' + new_json.side_text + ' <br>' + new_json.paper_text + '<br>' + new_json.deal_text + ' ' + new_json.amount + '건' +
            '<br><b class="price_cart">' + comma(Math.round(new_json.price*1.1)) + '</b>원 </span>' +
            '<br><i class="fas fa-truck text-muted" style="font-size: 10px;">&nbsp</i><small class="delivery_cart text-muted">' + comma(parseInt(new_json.delivery)) + ' </small></div>'
        );
    }


    $(document).ready(function () {
        var $loading_option = $('.loading-option');
        $cart_empty_message = $('.cart_empty_message');
        var $add_cart = $('#add_cart');

        $.ajax({
        type:"GET",
        url:"/design/cart/",
        dataType : "json",
        success: function(data){
            $.each(data, function (index, item) {
                cartList(item);
                $cart_empty_message.hide();
                $loading_option.show();
            });
             $loading_option.hide();
        }
        });

        $add_cart.click(function () {
            $add_cart.attr("disabled",true);
            setTimeout(function() {$add_cart.attr("disabled",false);}, 3000);
            $cart_empty_message.hide();
            var price = uncomma($('#sell_price').text());
            var title =  $.trim($('#title_name').text());
            var $memo =  $('#memo');
            var memo = $memo.val();
            var kind =  $.urlParam('item');
            var size_text = $("#size option:selected").text();
            var paper_text = $("#paper option:selected").text();
            var side_text = $("#side option:selected").text();
            var deal_text = $("#deal option:selected").text();
            var amount_text = $("#amount option:selected").val();
            var delivery_text = uncomma($("#delivery_price").text());
            var json_text = {
                    'title':title,
                    'kind':kind,
                    'size': size_default,
                    'size_text':size_text,
                    'paper': paper_default,
                    'paper_text':paper_text,
                    'side': side_default,
                    'side_text':side_text,
                    'deal': deal_default,
                    'deal_text':deal_text,
                    'amount':amount_text,
                    'price':price,
                    'delivery':delivery_text,
                    'memo':memo
                };
            $.ajax({
                type: "POST",
                url: "/design/cart/",
                dataType: "json",
                data: json_text,
                success: function (data) {
                    $memo.val('');
                    cartList(data);
                }
            });
        });
    });

     function cart_delete(obj) {
         var result = confirm('정말 삭제하시겠습니까?');
         if(result) {
             var num = obj.attr('name');
             $.ajax({
                type: "delete",
                url: "/design/cart/",
                dataType: "json",
                data: {'num':num},
                success: function (data) {
                    obj.parent().remove();
                    var $cart_delete_len = $('.cart_delete_btn').length;
                    if($cart_delete_len === 0){$cart_empty_message.show();}
                }
            });
         }
     }

     $.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
};