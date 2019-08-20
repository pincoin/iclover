  $(document).ready(function () {
        $select_tax_cla = $(".tax_select");
        var $id_company = $('#id_company');
        $product_result = $("#product_result");
        $product_search = $("#product_search");
        $search_result = $("#search_result");
        custromer ={};
        custromer['id'] = null;
        $("#id_company :input:text:first").focus();
        $id_company.keyup(delay(function (e) {
            var search_val = $id_company.val();
            $.ajax({
                url: '/api/profile.json',
                dataType: 'json',
                data: {'keyword': search_val},
                contentType: 'application/json; charset=UTF-8',
                success: function (data, status, xhr) {
                    $product_result.html('');
                    $product_search.val('');
                    $search_result.html('');
                    var index_num = 0;
                    var max_num = 4;
                    var count = data['count']-max_num;
                    data_list = {};
                    $.each(data['results'], function (key, item) {
                        var company = item.company;
                        var company_keyword = item.company_keyword;
                        if (search_val != '') {
                            if (index_num < max_num) {
                                $search_result.append(
                                    '<li class="list-group-item link-class text-custom"  id="' + item.id +
                                    '">' + company + ' | <span class="text-muted">' + company_keyword + '</span></li>'
                                );
                                data_id = item.id;
                                data_list[data_id] = item;
                                index_num += 1;
                            } else {
                                $search_result.append(
                                    '<li class="list-group-item link-class text-danger"><i class="mdi mdi-alert-octagon"></i><b> +'+ count+ '</b>...더 자세히 검색해주세요</li>'
                                );
                                index_num = 0;
                                return false;
                            }
                        }
                    })
                }
            });
        }, 300));
        $search_result.on('click', 'li', function () {
            $('.data-buttons').attr('style','');
            var idx = $(this).attr('id');
            if (idx) {
                custromer = data_list[idx];
                var click_text = $(this).text().split('|');
                $id_company.val($.trim(click_text[0]));
                $('#id_code').val(custromer['code']);
                $('#id_company_keyword').val(custromer['company_keyword']);
                $('#id_option').val(custromer['options']);
                $('#id_confirm').val(custromer['confirm']);
                $('#id_address').val(custromer['address']);
                $('#id_tell').val(custromer['tell']);
                $('#id_fix_manager').val(custromer['manager']);
                $('#id_memo').val(custromer['memo'].replace(/<br\s?\/?>/g,"\n"));
                $('#id_manager').val(custromer['manager']).attr('selected','selected');
                $search_result.html('');
                informations_html =
                    ('<b>'+custromer['company'] + '</b><br>' +
                    custromer['company_keyword'] + '<br>' +
                    custromer['code'] + '<br>' +
                    custromer['address'] + '<br>' +
                    custromer['tax_bill_mail'] + '<br>' +
                    custromer['tell'] + '<br>' +
                    custromer['phone'] + '<br>' +
                    custromer['keywords'] + '<br>' +
                    custromer['memo'] + '<br>' +
                    custromer['options'] + '<br>' +
                    custromer['confirm'] + '<br>' +
                    custromer['manager']);
                $("#informations").html(informations_html);
                $('input[id="product_search"]').focus();
                data_list = {};
            }
        });


        $product_search.keyup(delay(function (e) {
            $product_result.html('');
            var search_val = $product_search.val();
            var index_num = 0;
            var max_num = 12;
            var max_text = 10;
            data_list = {};
            if (search_val != '') {
                    $.ajax({
                        type: "GET",
                        url: '/api/product.json',
                        dataType: 'json',
                        data : {'idx' :custromer['id'],
                                'keyword': search_val,
                        },
                        success: function (data, status, xhr) {
                            $.each(data, function (key, item) {
                                var company = item.title;
                                var company_name = item.company_name;
                                var horizontal = item.horizontal;
                                var vertical = item.vertical;
                                var etc = item.etc;
                                var gram = item.gram;
                                var memo = item.memo;
                                var standard = item.standard;
                                var sell_price = item.sell_price;
                                var buy_price = item.buy_price;
                                if(horizontal && vertical){
                                    var ho_ver = parseInt(horizontal) + 'x' + parseInt(vertical);
                                }else{
                                     var ho_ver = '';
                                }
                                $product_result.append(
                                    '<a><span></span><div class="list-group-item link-class m-b-5 col-lg-12" style="height:80px;" id="' +
                                    '' + item.id + '"><b>' + company + '&nbsp&nbsp' + ho_ver +
                                    '</b>&nbsp&nbsp<b class="text-teal">' + company_name + '</b>' +
                                    '&nbsp<span class="text-muted">' + gram + '</span>' +
                                    '<br> <b class="text-dark" style="font-size: 18px;">' + comma(parseInt(sell_price)) + '</b>' +
                                    '&nbsp&nbsp<span class="text-muted">' + memo + '</span>' +
                                    '&nbsp&nbsp<span class="text-muted">' + etc + '</span>' +
                                    '</div></a>'
                                );
                                data_id = item.id;
                                data_list[data_id] = item;
                            })
                        }
                    });
            }
        }, 300));

            $product_result.on('click', 'div', function () {
            var idx = $(this).attr('id');
            if (idx) {
                product = data_list[idx];
                console.log(product);
                if(product['buy_price'] % 1 !== 0){var buy_price = product['buy_price'].toFixed(4)}else{var buy_price = parseInt(product['buy_price'])}
                if(product['sell_price'] % 1 !== 0){var sell_price = product['sell_price'].toFixed(4)}else{var sell_price = parseInt(product['sell_price'])}
                if(product['sell_price'] % 1 !== 0){var price_s = product['sell_price'].toFixed(4)}else{var price_s = parseInt(product['sell_price'])}
                if(product['buy_price'] % 1 !== 0){var buy_price = product['buy_price'].toFixed(4)}else{var buy_price = parseInt(product['buy_price'])}
                if($select_tax_cla.val() == '0'){var sell_price_tax = comma((product['sell_price']/10).toFixed(0))}else{sell_price_tax = 0}
                if (product['horizontal'] && product['vertical']) {
                    var ho_ver = parseInt(product['horizontal'])+'*'+parseInt(product['vertical'])
                } else {
                    var ho_ver = '';
                }
                 $('#sortable').append(
                    '<tr><td><span class="text_data"></span></td>' +
                     '<input class="form-control" type="hidden" name="text_data" value="'+ parseInt(product['code'])+'">' +
                     '<td><input class="form-control" type="text" name="text_data" value="'+product['standard']+'"></td>' +
                     '<td><input class="form-control" type="text" name="text_data" value="'+ho_ver+'"></td>' +
                     '<td><input class="form-control text-right quantity text_num" onkeyup="inputNumberFormat(this)" type="text" name="text_data" value="'+ parseInt(product['quantity'])+'"></td>' +
                     '<td><input class="form-control text-right price_s text_num" onkeyup="inputNumberFormat(this)" type="text" name="text_data" value="'+  comma(price_s)+'"></td>' +
                     '<td><input class="form-control text-right sell_price text_num" onkeyup="inputNumberFormat(this)" type="text" name="text_data" disabled value="'+  comma(sell_price)+'"></td>' +
                     '<td><input class="form-control text-right sell_tax text_num" onkeyup="inputNumberFormat(this)" type="text" name="text_data" disabled value="'+ sell_price_tax+'"></td>' +
                     '<td class="has-ask"><input class="form-control text-right buy_price text_num" onkeyup="inputNumberFormat(this)" type="text" name="text_data" value="'+ comma(buy_price)+'"></td>' +
                     '<input class="form-control" type="hidden" name="text_data" value="'+product['company_name']+'">' +
                     '<td><input class="form-control" type="text" name="text_data" value="'+product['gram']+'"></td>' +
                     '<td><input class="form-control" type="text" name="text_data" value="'+product['etc']+'"></td>' +
                     '<td><input class="form-control" type="text" name="text_data" value="'+product['memo']+'"></td>' +
                     '<td><a href="" class="table-action-btn h3 delete-button" style="display: none;" onclick="$(this).parent().parent().remove();return false;"><i class="mdi mdi-close-box-outline text-danger"></i></a></td>'+
                     '</tr>'
                 ).ready(function () {
                        SortableSpan();
                         Total()
                     })
            }
        });
    });

    $select_tax_cla.on("change", function () {
        var $sell_tax = $('.sell_tax');
        $sell_tax.each(function (key, data) {
            if ($select_tax_cla.val() == '0') {
                var sellprice = uncomma($(this).parent().parent().find('input.sell_price').val());
                $(this).val(comma((sellprice / 10).toFixed(0)));
            } else {
                $(this).val(0);
            }
        });
        $product_result.html('');
        $product_search.val('');
        Total();
    });

    $(function () {
        $("#sortable").sortable({
            update: function (event, ui) {
                SortableSpan();
                Total();
            }
        });
    });

    setTimeout(function() { $('input[name="company"]').focus() }, 500);
