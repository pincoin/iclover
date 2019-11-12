   function delay(fn, ms) {
        let timer = 0;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(fn.bind(this, ...args), ms || 0)
        }
    }

    function SortableSpan() {
        $('#sortable span').each(function (i) {
            var numbering = i + 1;
            $(this).text(numbering + '.');
        });
    }

    //콤마찍기
    function comma(str) {
        var parts = str.toString().split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        if(parts[0].length >2 ){ parts[0] = parts[0].replace(/(^0+)/, "");}
        return parts.join(".");
    }

    //콤마풀기
    function uncomma(str) {
        str = String(str);
        return str.replace(/[,]/g, "");
    }

    //값 입력시 콤마찍기 onkeyup="inputNumberFormat(this)"
    function inputNumberFormat(obj) {
        obj.value = comma(uncomma(obj.value));
    }


    function Total() {
        var $total_quantity = $('#total_quantity');
        var $total_price = $('#total_price');
        var $total_tax = $('#total_tax');
        var $total = $('#total');
        var $total_tr = $('.total-tr');
        var total_price = 0;
        var total_tax = 0;
        var total_quantity = 0;
        var total_buy = 0;

        $('#sortable tr').each(function () {
            var eq4 = $(this).children().eq(4).children().val();
            var eq5 = $(this).children().eq(6).children().val();
            var eq6 = $(this).children().eq(7).children().val();
            eq4 = uncomma(eq4); //수량
            eq5 = uncomma(eq5); //판매가
            eq6 = uncomma(eq6); //부가세
            total_quantity += parseFloat(eq4);
            total_price += parseFloat(eq5);
            total_tax += parseFloat(eq6);
        });
        var total =  total_price + total_tax;
        if(total_quantity != 0){
            $total_quantity.text(comma(total_quantity.toFixed(0)));
            $total_price.text(comma(total_price.toFixed(0)));
            $total_tax.text(comma(total_tax.toFixed(0)));
            $total.text('판매 합계 : '+comma(total.toFixed(0)));
            $total_tr.attr('style','background-color: #f3f3f3');
        }else{
            $total_quantity.text('');
            $total_price.text('');
            $total_tax.text('');
            $total.text('');
            $('#compare_price').html('');
            $total_tr.attr('style','background-color: #ffffff');
        }
    }

 /*  ----------------------선언 함수 ------------------------      */


     $(document).on("click",".delete-button",function() {
            SortableSpan();
            Total();
    });
      $(document).on("keyup",".sell_price",function() {
            var pre = uncomma($(this).val());
            pre = pre/10;
            $(this).parent().next().children().val(comma(pre.toFixed(0)));
            Total();
    });


    $("#sub-btn").click(function(e) {
        var list = new Array();
        $("input[name=text_data]").each(function (index, item) {
            list.push($(item).val());
        });
        $('#id_json_data').val(list.join('#,,#'));
    });

     $(document).on("keyup",".text_num",function() {
         if( !$(this).val()){
             $(this).val(0);
         }
            Total();
    });


      $(document).on("keyup",".quantity",function() {
            var quantity = uncomma($(this).val());
            var sell_price= uncomma($(this).parent().parent().find('input.price_s').val());
            var total = parseFloat(quantity)*parseFloat(sell_price);
            $(this).parent().parent().find('input.sell_price').val(comma(total));
             if ($select_tax_cla.val() == '0') {
                 $(this).parent().parent().find('input.sell_tax').val(comma((total / 10).toFixed(0)));
             }else{
                 $(this).parent().parent().find('input.sell_tax').val(0);
             }
            Total();
    });
      $(document).on("keyup",".price_s",function() {
            var price_s = uncomma($(this).val());
            var quantity= uncomma($(this).parent().parent().find('input.quantity').val());
            var buy_price= uncomma($(this).parent().parent().find('input.buy_price').val());
            var total = parseFloat(quantity)*parseFloat(price_s);
            var compare = parseFloat(price_s)-parseFloat(buy_price);

           var $td = $(this).parent().parent().find('input.buy_price');

            if(compare < 0){
                $td.parent().attr('class','has-special');
            }else{
                $td.parent().attr('class','has-ask');
            }
            $(this).parent().next().children().val(comma(total));
            if ($select_tax_cla.val() == '0') {
                $(this).parent().parent().find('input.sell_tax').val(comma((total/10).toFixed(0)));
            }else{
                 $(this).parent().parent().find('input.sell_tax').val(0);
             }
            Total();
    });

      $(document).on("keyup",".buy_price",function() {
          var $td = $(this).parent().parent().find('input.buy_price');
          var buy_price = uncomma($(this).val());
          var price_s= uncomma($(this).parent().parent().find('input.price_s').val());
          var compare = parseFloat(price_s)-parseFloat(buy_price);
            if(compare < 0){
                $td.parent().attr('class','has-special');
            }else{
                $td.parent().attr('class','has-ask');
            }
      });

    $(document).on("keydown","input[type=text]",function() {
        if (event.keyCode === 13) {
        event.preventDefault();
        }
    });



    $("#delete_check").click(function() {
        if($('input:checkbox[id="delete_check"]').is(":checked") == true){
             $(".delete-button").show();
        }else{
            $(".delete-button").hide();
        }
         SortableSpan();
    });


    /*  ---------- 지난 데이터 ------------ */
    var $control_info = $('#control-info');
    var $control_order = $('#control-order');
    var $load_more = $('#load_more');
    var $load_btn = $('#load_btn');
    var $list_info = $('.list_info');
    var $list_order = $('.list_order');
    var order_cache = false;
    $control_info.click(function () {
        $list_info.show();
        $list_order.hide();
        $load_more.hide();
         $load_btn.attr('href','');
    });

    function call_load(){
        var url = $load_btn.attr('href');
        if(!url){
            url ='/rowapi/order_info.json';
            $list_order.text('');
        }else{
            url = url;
        }
        $list_order.show();
        $list_info.hide();
        $.ajax({
          url: url,
          dataType: 'json',
          data: {'keyword': custromer['id']},
          contentType: 'application/json; charset=UTF-8',
          success: function (data, status, xhr) {
                order_cache =true;
                if(data['count']==0){
                    $list_order.text('지난 과거 데이터가 없습니다.');
                }else{
                    /* 'id','name','quantity','selling_price' */
                        $.each(data['results'], function(index, val){
                            var good = [5,6,7];
                            var state = val.state;
                            var color = '';
                            if($.inArray(state, good)){
                                color = 'panel-default';
                                info_text = '정상';
                            }else{
                                color = 'panel-danger';
                                info_text = '취소/보류/환불';
                            }
                            var val2_list = new(Array);
                            $.each(val.order_list, function(ind, val2){
                               val2_list += val2.name + ' / '+ comma(Math.round(val2.selling_price))+'<br>'
                            });
                          var json_data =
                            '<div class="m-t-5 m-r-15 panel panel-border '+color+'">' +
                            '<div class="panel-heading">' +
                            '<h3 class="panel-title">'+val.joo_date+'_'+val.today_num+ '<small> '+info_text +
                              ' <a class="id_info" id="'+ val.id+'"style="cursor:pointer"><i class="fa fa-plus text-teal"></i></a></small></h3>' +
                            '</div>' +
                            '<div class="panel-body">' +
                            val2_list
                             +'</div>' +
                            '</div>';
                            $list_order.append(json_data);
                        });
                        if(data['next']){
                            $load_more.show();
                             $load_btn.attr('href',data['next']);
                        }else{
                            $load_more.hide();
                        }
                }
          }
      });
    }

    $control_order.click(function () {
        call_load();
    });
    $load_btn.click(function () {
        call_load();
    });
     $(document).on("click",".id_info",function() {
            console.log($(this).attr('id'));
    });
