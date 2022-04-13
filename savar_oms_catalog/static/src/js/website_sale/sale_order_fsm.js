odoo.define('savar_oms_catalog.web_editor_sale_order_fsm', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var dialog = require('web.Dialog');
    var _t = core._t;

    publicWidget.Widget.include(
    {
        
        init: function (parent, action) 
        {            
            var self = this;
            this.fsm_order = null;
            self.init_order_fsm_ecommerce();
            self.init_order_fsm_service();
            self.init_order_fsm_payment_type();
            self.init_order_fsm_by_packages();
            self.init_order_fsm_countries();
            self.init_order_fsm_states();
            self.init_order_fsm_provinces();
            self.init_order_fsm_districts(); 
            
            $( document ).ready(function() 
            {
                console.log("table.table_stock_moves input.stock_move_product");
                $('table.table_stock_moves input.stock_move_product').first().click();
                $('table.table_stock_moves input.stock_move_location_id').first().click();
                $('table.table_stock_moves input.stock_move_quantity_on_hand').first().val(parseInt(1));
                $("#fsm_ends_appointment").val("8_30_am");
                self.validate_appointment_times();    
                $("#fsm_zip").attr("disabled", true);            
            
                $('input#fsm_order_ref').unbind('blur');          
                $('input#fsm_order_ref').blur(function(event)
                {
                    var response = self.get_fsm_order();            
                    response.then(self.get_fsm_order_callback);
                });

                $('div#upload_massive_orders').unbind('click');          
                $('div#upload_massive_orders').click(function(event)
                {                
                    var attachment = $('input[name="attachment"]').val();
                    if(attachment)
                    {
                        if($('input#fsm_orders').length>0)
                        { $(this).closest('form').attr('action', '/orders/massive_save_fsm') }
                        else
                        { $(this).closest('form').attr('action', '/orders/massive_save') }
                        $(this).closest('form').find('input#massive_save_button').click();
                    }
                    else
                    {
                        event.preventDefault();
                        dialog.alert(null, String("Explore y seleccione archivo Excel."), {});
                    }
                });

                $('div#export_xls_button').unbind('click');          
                $('div#export_xls_button').click(function(event)
                {                
                    event.preventDefault();
                    $("form#massive_export_xls").submit(function(){
                        self.update_xlsx_templates_board();
                    });
                });

                $('a.save_fsm_order').unbind('click');
                $("a.save_fsm_order").bind('click');
                $("a.save_fsm_order").click(function(event){ 
                    event.preventDefault();
                    console.log("a.save_fsm_order");
                    self.save_merchant_fsm_order($(this));
                });

                $('input#fsm_service').unbind('click');
                $("input#fsm_service").bind('click');
                $("input#fsm_service").click(function(event)
                {
                    console.log("init_order_fsm_subservice");
                    event.preventDefault();
                    self.init_order_fsm_subservice();
                });

                $('input#fsm_country_id').unbind('click');
                $("input#fsm_country_id").click(function(event)
                {
                    console.log("init_order_fsm_states");
                    event.preventDefault();
                    self.init_order_fsm_states();
                });

                $('input#fsm_state_id').unbind('click');
                $("input#fsm_state_id").click(function(event)
                {
                    console.log("init_order_fsm_provinces");
                    event.preventDefault();
                    self.init_order_fsm_provinces();
                });

                $('input#fsm_province_id').unbind('click');
                $("input#fsm_province_id").click(function(event)
                {
                    console.log("init_order_fsm_districts");
                    event.preventDefault();
                    self.init_order_fsm_districts();
                });   

                $('a.add_form_fsm_line').off('click');
                $('a.add_form_fsm_line').click( function (event) 
                {
                    console.log('a.add_form_fsm_line');
                    event.preventDefault();
                    self.add_form_stock_move();
                    $('table.table_stock_moves').find('tr').last().find('input.stock_move_product').last().click();
                    $('table.table_stock_moves').find('tr').last().find('input.stock_move_location_id').last().click();
                    $('table.table_stock_moves').find('tr').last().find('input.stock_move_uom').last().click();
                    $('table.table_stock_moves').find('tr').last().find('input.stock_move_quantity_on_hand').last().val(parseInt(1));
                }); 

                $('input.stock_move_uom').off('click');
                $("body").on('click', 'input.stock_move_uom', function(event)
                {
                    event.preventDefault();
                    var product_id = $('table.table_stock_moves').find('tr').last().find('input.stock_move_product').last().val();
                    console.log('stock_move_uom product_id');
                    console.log(product_id);
                    try
                    {
                        if(parseInt(product_id)>0)
                        {
                            var params = {
                                '_selector':$('table.table_stock_moves').find('tr').last().find('input.stock_move_uom').last(),
                                '_route':'/selections/product/get_uoms',
                                '_fields':['id', 'name'],
                                '_domain':[['product_id','=',parseInt(product_id)]],
                                '_multiple':false,
                            } 
                            self._start_any_select2_003(params);
                            var uom = {
                                        id: 1,
                                        text: 'Unidades'
                                    };
                                
                            var default_uom = new Option(uom.text, uom.id, false, false);
                            console.log('default_uom');
                            console.log(default_uom);
                            $('table.table_stock_moves').find('tr').last().find('input.stock_move_product').last().append(default_uom).trigger('change');
                            $('table.table_stock_moves').find('tr').last().find('input.stock_move_product').last().val('');
                        }
                    }
                    catch(error)
                    {
                        $('table.table_stock_moves').find('tr').last().find('input.stock_move_product').last().val('');
                    }

                });
                
                $('input.stock_move_product').unbind('change');
                $("body").on('change', 'input.stock_move_product', function(event)
                {
                    console.log("change input.stock_move_product");
                    $(this).closest('tr').find('input.stock_move_uom').click();;
                });
                
                $('input.stock_move_product').off('click');
                $("body").on('click', 'input.stock_move_product', function(event)
                {
                    console.log("input.stock_move_product");
                    event.preventDefault();                
                    var params = {
                        '_selector': $('table.table_stock_moves').find('tr').last().find('input.stock_move_product').last(),
                        '_route':'/selections/products/get_products',
                        '_fields':['id', 'name'],
                        '_domain':[],
                        '_multiple':false,
                    }
                    self._start_any_select2_003(params);
                });

                $('input.stock_move_location_id').off('click');
                $("body").on('click', 'input.stock_move_location_id', function(event)
                {
                    event.preventDefault();
                    var params = {
                        '_selector':$('table.table_stock_moves').find('tr').last().find('input.stock_move_location_id').last(),
                        '_route':'/selections/stock/get_locations',
                        '_fields':['id', 'name'],
                        '_domain':[],
                        '_multiple':false,
                    }
                    self._start_any_select2_003(params);
                });            

                $('select.fsm_start_appointment').off('click');
                $("body").on('click', 'select.fsm_start_appointment', function(event)
                {
                    event.preventDefault();                
                    self.validate_appointment_times();
                });

                $('select.fsm_ends_appointment').off('click');
                $("body").on('click', 'select.fsm_ends_appointment', function(event)
                {
                    event.preventDefault();                
                    self.validate_appointment_times();
                });
            });
            this._super(parent, action);
        },        
        validate_appointment_times: function()
        {
            var index_start_date  = $("#fsm_start_appointment option:selected").index();
            var index_end_date  = $("#fsm_ends_appointment option:selected").index();
            console.log("index-option-index_start_date");
            console.log(index_start_date);
            $("#fsm_ends_appointment option").show();
            $("#fsm_ends_appointment option").each(function(index)
            {
                var option = $(this);
                
                if(index <= index_start_date)
                {                    
                    option.hide();
                }
                if(index_start_date>=index_end_date)
                {
                    $('#fsm_ends_appointment option').eq(index_start_date+1).prop('selected', true);
                }
            });
            
        },
        validate_inventory_lines: function()
        {
            var response = {'error':false,'message':''}
            var message = String();
            var has_errors = Boolean(false);

            $("table.table_stock_moves tr.stock_move").each(function(index)
            {
                var _stock_move = $(this);
                
                var product_id = _stock_move.find('input.stock_move_product').val();
                var location_id = _stock_move.find('input.stock_move_location_id').val();
                var quantity = _stock_move.find('input.stock_move_quantity_on_hand').val();
                var stock_move = {
                                    'product_id': (product_id),
                                    'location_id': (location_id),
                                    'quantity': (quantity),
                                 };
                try
                { 
                    if(parseInt(stock_move['product_id']) && parseFloat(stock_move['product_id'])>0 && parseFloat(stock_move['location_id'])!=NaN)
                    {}
                    else
                    {
                        message +=  String('- Producto debe ser establecida. </br>');
                        has_errors = true;
                    }  
                }
                catch(error)
                {
                    has_errors = true;
                }

                try
                {   
                    if(parseInt(stock_move['location_id']) && parseFloat(stock_move['location_id'])>0 && parseFloat(stock_move['location_id'])!=NaN)
                    {}
                    else
                    {
                        message +=  String('- Ubicación debe ser establecida. </br>');
                        has_errors = true;
                    } 
                }
                catch(error)
                {
                    has_errors = true;
                }
                
                try
                { 
                    if(parseFloat(stock_move['quantity']) && parseFloat(stock_move['quantity'])>0)
                    {} 
                    else
                    {
                        message +=  String('- La cantidad debe ser mayor a cero. </br>');
                        has_errors = true;
                    }
                }
                catch(error)
                {
                    has_errors = true;
                }
                
                if(has_errors==true)
                {
                    var product_id_label = _stock_move.find('input.stock_move_product').select2('data');
                    if(product_id_label)
                    {
                        if(product_id_label.text)
                        {
                            message = String('Movimiento: ') + String(product_id_label.text) + String('</br>') + String(message);
                        } 
                        else
                        {
                            message = String('Movimiento: #') + String(index) + String('</br>') + String(message);
                        }                         
                    }
                    else
                    {
                        message = String('Movimiento: #') + String(index) + String('</br>') + String(message);
                    } 
                }

                response['message'] += message;
                response['error'] = has_errors;

                message = String();
                has_errors = Boolean(false);
                
            });   
            return response;
        },
        get_fsm_order: function()
        {
            var self = this;
            var fsm_order_ref = $('#fsm_order_ref').val();
            var order_name = $('input[name="order_name"]').val();

            var _params = {
                            'fsm_order_ref':fsm_order_ref, 
                            'order_name':order_name
                          }
            
            var def = new $.Deferred();            
                          
            return rpc.query({
                model: "fsm.order",
                method: "get_merchant_fsm_order",
                args: ["", _params],
            }).then((order,) =>
            {
                
                if(order)
                {         
                    self.fsm_order = order;
                    def.resolve();
                    return order;
                }
            });
        },
        get_fsm_order_callback: function(order)
        {
            if(order)
                {
                    var fsm_order_ref = $('input#fsm_order_ref').val();
                    var message = 'El pedido de trabajo ' + String(fsm_order_ref) + ' ya se encuentra creada.';
                    dialog.alert(self, '', {
                        title: _t("Pedido de trabajo"),
                        $content: $('<div/>').html(message)
                    });
                    return true;
                }
                return false;
        },   
        add_form_stock_move: function () 
        {
            var default_stock_move = $('table.default_stock_move_table').find('tbody');
            var _html = default_stock_move.html();
            var remove_action = default_stock_move.find('div.action_remove_stock_move');
            $('table.table_stock_moves').append(_html);
        },
        init_order_fsm_appointments: function()
        {            
            rpc.query( {
                model: "fsm.order",
                method: "get_appointments_range_time",
                args: [""],
            }).then((ranges) => 
            {
                console.log(ranges);
                if(ranges)
                {
                    ranges.forEach(function(time)
                    {
                        
                    });
                }
            });
        },             
        save_merchant_fsm_order: function()
        {
            var self = this;           

            var response = self.validate_inventory_lines();
            
            if(response['error']==true)
            {
                if($('.modal-dialog').length==0)
                {
                    dialog.alert(self, '', {
                        title: _t("Pedido de trabajo"),
                        $content: $('<div/>').html(response['message'])
                    });
                }
                return false;
            }

            var name = $('input[name="order_name"]').val();
            var reference = $('input[name="fsm_reference"]').val();
            var service = $('input[name="fsm_service"]').val();
            var subservice = $('input[name="fsm_subservice"]').val();
            var fsm_payment_type_id = $('input[name="fsm_payment_type_id"]').val();
            var fsm_consigned_id = $('input[name="fsm_consigned_id"]').val();
            var fsm_shipping_type_id = $('input[name="fsm_shipping_type_id"]').val();
            var fsm_by_package_id = $('input[name="fsm_by_package_id"]').val();
            
            var fsm_country_id = $('input[name="fsm_country_id"]').val();
            var fsm_state_id = $('input[name="fsm_state_id"]').val();
            var fsm_province_id = $('input[name="fsm_province_id"]').val();
            var fsm_district_id = $('input[name="fsm_district_id"]').val();
            var fsm_code = $('input[name="fsm_zip"]').val();

            var fsm_start_time = $("#fsm_start_appointment").val();
            var fsm_ends_time = $("#fsm_ends_appointment").val();

            var date_dispatch = $("#fsm_dispatch").val();
            
            var _stock_quants = []
            $("table.table_stock_moves tr.stock_move").each(function()
            {
                console.log("tr.stock_move");
                var stock_move = $(this);
                var product_id = stock_move.find('input.stock_move_product').val();
                var location_id = stock_move.find('input.stock_move_location_id').val();
                var uom_id = stock_move.find('input.stock_move_uom').val();
                var on_hand = stock_move.find('input.stock_move_quantity_on_hand').val();
                var stock_quant = {
                                    'product_id': parseInt(product_id),
                                    'location_id': parseInt(location_id),
                                    'uom_id': parseInt(uom_id),
                                    'quantity': parseInt(on_hand),
                                  }
                console.log("stock_quant");
                console.log(stock_quant);
                _stock_quants.push(stock_quant);
            });
            var fsm_start_time = $("#fsm_start_appointment").val();
            var fsm_ends_time = $("#fsm_ends_appointment").val();

            var _order = {
                            'name': name, 
                            'code_merchant': reference, 
                            'service_id': service, 
                            'subservice_id': subservice, 
                            'shipping_type_id': fsm_shipping_type_id, 
                            'by_package_id': fsm_by_package_id, 
                            'payment_type_id': fsm_payment_type_id, 
                            'consigned_id': fsm_consigned_id,
                            'fsm_start_time': fsm_start_time,
                            'fsm_ends_time': fsm_ends_time,
                            'date_dispatch': date_dispatch,
                            'location':{
                                         'country_id':fsm_country_id,
                                         'state_id':fsm_state_id,
                                         'province_id':fsm_province_id,
                                         'district_id':fsm_district_id,
                                         'code':fsm_code,
                                       },
                            'stock_quants':_stock_quants
                         }
            
            console.log('save_merchant_fsm_order _order');
            console.log(_order);

            rpc.query( {
                            model: "fsm.order",
                            method: "create_merchant_fsm_order",
                            args: ["", _order],
                        }).then((reponse) => 
                        {
                            if(reponse)
                            {
                                if(reponse.hasOwnProperty('error'))
                                {
                                    var fsm_order_ref = $('input#fsm_order_ref').val();
                                    var message = 'El pedido de trabajo ' + String(fsm_order_ref) + ' ya se encuentra creada.';
                                    dialog.alert(self, '', {
                                        title: _t("Pedido de trabajo"),
                                        $content: $('<div/>').html(message)
                                    });
                                }       

                            }
                        });
        },
        init_order_fsm_countries: function()
        {
            var self = this;
            var params = {
                            '_selector':$("input#fsm_country_id").first(),
                            '_route':'/selections/orders/fsm_location_contries',
                            '_fields':['id', 'name'],
                            '_domain':[],
                            '_multiple':false,
                         }
                         
            self._start_any_select2_003(params);
        },
        init_order_fsm_states: function()
        {
            var self = this;
            var country_id = $("input#fsm_country_id").val();
            console.log('init_order_fsm_countries country_id');
            console.log(country_id);
            var params = {
                            '_selector':$("input#fsm_state_id").first(),
                            '_route':'/selections/orders/fsm_location_states',
                            '_fields':['id', 'name'],
                            '_domain':[
                                        ['country_id', '=', parseInt(country_id)],
                                        ['state_id', '=', null],
                                        ['province_id', '=', null],
                                      ],
                            '_multiple':false,
                         }                         
            self._start_any_select2_003(params);
        },
        init_order_fsm_provinces: function()
        {
            var self = this;
            var country_id = $("input#fsm_country_id").val();
            var state_id = $("input#fsm_state_id").val();
            console.log('init_order_fsm_countries country_id');
            console.log(country_id);
            console.log(state_id);
            var params = {
                            '_selector':$("input#fsm_province_id").first(),
                            '_route':'/selections/orders/fsm_location_provices',
                            '_fields':['id', 'name'],
                            '_domain':[
                                        ['country_id', '=', parseInt(country_id)],
                                        ['state_id', '=', parseInt(state_id)],
                                        ['province_id', '=', null],
                                      ],
                            '_multiple':false,
                         }                         
            self._start_any_select2_003(params);
        },
        init_order_fsm_districts: function()
        {
            var self = this;
            var country_id = $("input#fsm_country_id").val();
            var state_id = $("input#fsm_state_id").val();
            var province_id = $("input#fsm_province_id").val();
            console.log('init_order_fsm_countries country_id');
            console.log(country_id);
            var params = {
                            '_selector':$("input#fsm_district_id").first(),
                            '_route':'/selections/orders/fsm_location_districts',
                            '_fields':['id', 'name', 'code'],
                            '_domain':[
                                        ['country_id', '=', parseInt(country_id)],
                                        ['state_id', '=', parseInt(state_id)],
                                        ['province_id', '=', parseInt(province_id)],
                                      ],
                            '_multiple':false,
                         }                         
            self._start_any_select2_003(params);
        },        
        init_order_fsm_by_packages: function()
        {
            var self = this;
            var params = {
                            '_selector':$("input#fsm_by_package_id").first(),
                            '_route':'/selections/orders/fsm_by_packages',
                            '_fields':['id', 'name'],
                            '_domain':[],
                            '_multiple':false,
                         }
                         
            self._start_any_select2_003(params);
        },
        init_order_fsm_payment_type: function()
        {
            var self = this;
            var params = {
                            '_selector':$("input#fsm_payment_type_id").first(),
                            '_route':'/selections/orders/fsm_payment_types',
                            '_fields':['id', 'name'],
                            '_domain':[],
                            '_multiple':false,
                         }
                         
            self._start_any_select2_003(params);
        },
        init_order_fsm_service: function()
        {
            var self = this;
            var params = {
                            '_selector':$("input#fsm_service").first(),
                            '_route':'/selections/service/get_services',
                            '_fields':['id', 'name'],
                            '_domain':[['parent_id','=',null]],
                            '_multiple':false,
                         }
                         
            self._start_any_select2_003(params);
        },
        init_order_fsm_ecommerce: function()
        {
            var self = this;
            var params = {
                            '_selector':$("input#fsm_account").first(),
                            '_route':'/selections/orders/get_fsm_account',
                            '_fields':['id', 'name'],
                            '_domain':[['is_ot_account','!=',null]],
                            '_multiple':false,
                         }
                         
            self._start_any_select2_003(params);

            var params = {
                '_selector':$("input#fsm_channel").first(),
                '_route':'/selections/orders/get_fsm_channel',
                '_fields':['id', 'name'],
                '_domain':[['is_ot_channel','!=',null]],
                '_multiple':false,
             }
             
            self._start_any_select2_003(params);
        },
        init_order_fsm_subservice: function()
        {
            var self = this;
            var parent_id = $("input#fsm_service").val();
            console.log("init_order_fsm_subservice parent_id");
            console.log(parent_id);
            try
            {
                var params = {
                                '_selector':$("input#fsm_subservice").first(),
                                '_route':'/selections/service/get_services',
                                '_fields':['id', 'name'],
                                '_domain':[['parent_id','=',parseInt(parent_id)]],
                                '_multiple':false,
                              }
                 
                self._start_any_select2_003(params);
            }
            catch(error)
            {
                console.log(error);
            }            
        },
        _start_any_select2_003: function (params) {            
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
                            if(String(params['_route'])==String("/selections/orders/fsm_location_districts"))
                            {
                                $("#fsm_zip").val(obj.code)
                            }
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