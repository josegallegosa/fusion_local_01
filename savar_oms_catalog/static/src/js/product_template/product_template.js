odoo.define('savar_oms_catalog.product_template', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    
    publicWidget.Widget.include({
        init: function (parent, action) 
        {
            var self = this;
            $('nav.merchant_navigation_nav li#edit-page-menu').unbind( "click" );
            $('nav.merchant_navigation_nav li#save-page-menu').unbind( "click" );
            $('nav.merchant_navigation_nav li#edit-page-menu').click(function (event) 
            {
                if(String( $("#edition_mode").val() ) == String("order"))
                {console.log("edit-page-menu 004")}
                else
                {
                    self.init_product_edition_001();
                }                                
            });
            
            $('nav.merchant_navigation_nav li#save-page-menu').click(function (event) 
            {
                event.preventDefault();
                self.save_product_taxes_edition_001();
            });

            /**
             * BG Evento Fantasma
             */
                $('.svc_product_id').unbind('click');
                $('.svc_product_id').off('click');
                $(document).on('click', '.svc_product_id', function (event) 
                {
                    event.preventDefault();
                    self.init_product_service();
                });
                $(document).ready(function()
                {
                    $('.svc_product_id').unbind('click');
                    $('.svc_product_id').off('click');
                    $(".svc_product_id").click();
                });
            /**
             * EOF Evento Fantasma
             */

            self._super(parent, action);
        }, 
        init_product_service: function()
        {
            var self = this;
            var params = {
                            '_selector':$("input.product_subservice").first(),
                            '_route':'/selections/service/get_services',
                            '_fields':['id', 'name'],
                            '_domain':[['parent_id','!=',null]],
                            '_multiple':true,
                         }
                         
            self._start_any_select2_002(params);
            self.init_merchant_product_service_assigned();
            var _subservices = $("input[name='product_subservice']").val();
            console.log(_subservices);
            self.preselection_product_service(params['_selector']);
        },
        preselection_product_service: function(selector){
            var self = this;
            var svc_product_id = $("span.svc_product_id").text();
            try
            {
                if(parseInt(svc_product_id))
                {}

                rpc.query({
                    route: '/selections/products/get_product_services',
                    params: {
                        product_id: svc_product_id,
                        fields: ['id','name'],
                    }
                }).then(function (subservices) {
                    if(subservices)
                    {
                        if(subservices.read_results)
                        {   
                            try                      
                            {
                                var _input_value = String();
                                var vector = subservices.read_results;
                                var _subservices_size = $("div.product_subservice").find('ul.select2-choices').find('li').length;
                                if(_subservices_size < vector.length)
                                {
                                    vector.forEach(function(subservice)
                                    {
                                        var li = $("<li class='select2-search-choice'/>");
                                        var li_text = $("<div>"+String(subservice.name)+"<div/>");
                                        var li_a_delete = $("<a href='#' class='select2-search-choice-close custom_tax_delete' tabindex='-1' data-id='"+String(subservice.id)+"' />");
                                        
                                        li_a_delete.on('click', function () 
                                        {
                                            self.delete_preselection_tag_003($(this));
                                        });

                                        var option = li.append(li_text).append(li_a_delete);                  
                                        selector.closest('tr').find("ul.select2-choices").prepend(option);

                                        _input_value = String(_input_value) + String(parseInt(subservice.id)) + String(",");
                                    });

                                    if( String(_input_value).length>0 )
                                    {
                                        _input_value = String(_input_value).slice(0, -1);
                                        selector.val(_input_value);
                                    }  
                                }                                
                            }
                            catch(e)
                            {}
                        }
                    }                   
                });               
            }   
            catch(error)
            {}
        },
        init_product_subservice: function()
        {
            var self = this;
            var product_service = $("input.product_service").val();
            if(product_service)
            {
                if(parseInt(product_service)>0)
                {
                    var params = {
                        '_selector':$("input.product_subservice"),
                        '_route':'/selections/service/get_services',
                        '_fields':['id', 'name'],
                        '_domain':[['parent_id','=',parseInt(product_service)]],
                     }
                    self._start_any_select2_002(params);
                    self.init_merchant_product_subservice_assigned(product_service);
                    var product_subservice = $("input.product_subservice").val();
                    console.log(String('product_subservice: ') + String(product_subservice));
                }                
            }
        },
        init_merchant_product_service_assigned: function()
        {
            console.log("populate service");
        },
        init_merchant_product_subservice_assigned: function()
        {
            console.log("populate subservice");   
        },       
        init_product_edition_001: function () {
            var self = this;
            self.enable_fields_for_edition_001();
            self.enable_product_list_price_001();
            self.init_product_service();
        },
        save_product_taxes_edition_001: function () {
            var self = this;
            self.save_values();
            self.disable_fields_for_edition_001();
            self.disable_fields_product_name_001();
            self.disable_fields_product_list_price_001();
        },
        save_values:function()
        {
          var _id = $(".js_publish_management").attr('data-id');
          var product_name = $("input#product_name").val();
          var product_list_price = $("#product_list_price").val();
          var taxes_id = $("#taxes_id").val();
          var taxes = [];
          
          try
          {
            taxes_id = String(taxes_id).split(',');
            taxes_id.forEach(function(tax){
                taxes.push(tax);
            });            
          }
          catch(e)
          {}

          var standard_price = $("input[name='standard_price']").val();
          var default_code = $("input[name='default_code']").val();
          var barcode = $("input[name='barcode']").val();
          var public_description = $("textarea[name='public_description']").html();
          var product_service = $('input.product_service').val();
          var product_subservice = $('input.product_subservice').val();
          var product_stock = $('input#product_stock').val();

          var params = {
            'id': _id,
            'name': product_name,
            'list_price': product_list_price,
            'taxes_id': taxes,
            'standard_price': standard_price,
            'default_code': default_code,
            'barcode': barcode,
            'public_description': public_description,
            'product_service': product_service,
            'product_subservice': product_subservice,
            'product_stock': product_stock,
        }

        rpc.query({
            model: "product.template",
            method: "save_values",
            args: ["", params],
            }).then(() => {});
        },
        enable_product_list_price_001: function()
        {
            var self = this;
            var _product_list_price_element = $('b.oe_price');
            var _product_list_price = _product_list_price_element.find('span.oe_currency_value').text();
            _product_list_price = self.money_to_float(_product_list_price);
            _product_list_price_element.find('span.oe_currency_value').hide();
            if(_product_list_price_element.find("input#product_list_price").length>0)
            {
                _product_list_price_element.find("input#product_list_price").val(_product_list_price);
            }
            else
            {
                _product_list_price_element.append('<input class="form-control" type="number" step="any" id="product_list_price" value="'+String(_product_list_price)+'"/>');   
            }
            _product_list_price_element.find("input#product_list_price").fadeIn();
        },
        disable_fields_product_list_price_001: function()
        {   
            var self = this;         
            var _product_list_price_element = $('b.oe_price');
            var _price = _product_list_price_element.find("input#product_list_price").val();
            _product_list_price_element.find("input#product_list_price").hide();
            _product_list_price_element.find('span.oe_currency_value').text(self.money_to_float(_price)).fadeIn();
        },
        money_to_float: function(money)
        {
            money = String(money).replace(',','');
            money = String(money).replace(',','');
            return money;
        },
        disable_fields_for_edition_001: function()
        {
            var self = this;
            $("#taxes_id").select2("readonly", true); 
            self.disable_product_extra_fields_001();       
        },
        enable_fields_for_edition_001: function()
        {
            var self = this;
            $("#taxes_id").select2("readonly", false);
            self.enable_product_name_001();
            self.enable_product_extra_fields_001();         
        },
        enable_product_name_001:function()
        {
            var self = this;
            var _product_name_element = $('h1[itemprop="name"]');
            _product_name_element.hide()
            var _product_name = _product_name_element.text();

            if($("input#product_name").length>0)
            {
                $("input#product_name").val(_product_name);
            }
            else
            {
                _product_name_element.before('<input class="form-control" type="text" id="product_name" value="'+String(_product_name)+'"/>');   
                $("input#product_name").val(_product_name);
            }           
        },
        disable_fields_product_name_001: function()
        {
            var _product_name_element = $('h1[itemprop="name"]');
            var _name = _product_name_element.find("input#product_name").val();
            $("input#product_name").remove();
            _product_name_element.text(_name);
            _product_name_element.fadeIn();
        },
        enable_product_extra_fields_001:function()
        {
            var self = this;
            // list_price
            self.label_looks_as_input_001($("input[name='list_price']"));
            // standard_price
            self.label_looks_as_input_001($("input[name='standard_price']"));            
            // default_code
            self.label_looks_as_input_001($("input[name='default_code']"));
            // barcode
            self.label_looks_as_input_001($("input[name='barcode']"));
            // public_description
            self.label_looks_as_input_001($("textarea[name='public_description']"));
            // stock virtual
            self.label_looks_as_input_001($("input[name='product_stock']"));
            // subservice
            $('.product_subservice').select2("readonly", false);
        },
        disable_product_extra_fields_001:function()
        {
            var self = this;
            // list_price
            self.input_looks_as_label_001($("input[name='list_price']"));
            // standard_price
            self.input_looks_as_label_001($("input[name='standard_price']"));
            // default_code
            self.input_looks_as_label_001($("input[name='default_code']"));
            // barcode
            self.input_looks_as_label_001($("input[name='barcode']"));
            // public_description
            self.input_looks_as_label_001($("textarea[name='public_description']"));
            // stock virtual
            self.input_looks_as_label_001($("input[name='product_stock']"));
            // subservice
            $('.product_subservice').select2("readonly", true);
        },
        input_looks_as_label_001:function(element)
        {
            element.addClass("input-as-label");
            element.attr('readonly','1');
        },
        label_looks_as_input_001:function(element)
        {
            element.removeClass("input-as-label");
            element.removeAttr('readonly');
        },
        _start_any_select2_002: function (params) {            
            var self = this;
            params['_selector'].select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: params["_multiple"],
                selection_data: false,
                formatSelection: function (data) 
                {
                    if (data.tag) {
                        data.text = data.tag;
                    }
                    return data.text;
                },
                createSearchChoice: function (term, data) {
                    var addedTags = $(this.opts.element).select2('data');
                    if (_.filter(_.union(addedTags, data), function (tag) {
                        return tag.text.toLowerCase().localeCompare(term.toLowerCase()) === 0;
                    }).length === 0) {
                        if (this.opts.can_create) {
                            return {
                                id: _.uniqueId('tag_'),
                                create: true,
                                tag: term,
                                text: _.str.sprintf(_t("Create new Tag '%s'"), term),
                            };
                        } else {
                            return undefined;
                        }
                    }
                },
                fill_data: function (query, data) {
                    var that = this,
                        tags = { results: [] };
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.name)) {
                            tags.results.push({ id: obj.id, text: obj.name });
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    if (!this.selection_data) {
                        rpc.query({
                            route: params['_route'],
                            params: {
                                fields: params['_fields'],
                                domain:  params['_domain'],
                            }
                        }).then(function (data) {
                            that.can_create = data.can_create;
                            that.fill_data(query, data.read_results);
                            that.selection_data = data.read_results;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }                    
                }
            });
        },
    });
});