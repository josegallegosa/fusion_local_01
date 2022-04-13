odoo.define('savar_oms_catalog.product_taxes', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    publicWidget.Widget.include({
        init: function (parent, action) {
            var self = this;            

            $('nav.merchant_navigation_nav li#save-page-menu').click(function (event) 
            {
                event.preventDefault();
                self.save_product_taxes_edition_002();
            });

            $('nav.merchant_navigation_nav li#edit-page-menu').unbind( "click" );
            $('nav.merchant_navigation_nav li#save-page-menu').unbind( "click" );
            $('nav.merchant_navigation_nav li#edit-page-menu').click(function (event) 
            {
                event.preventDefault();                
                if(String( $("#edition_mode").val() ) == String("order"))
                {}
                else
                {
                    self.init_product_taxes_edition_002();
                    self._start_taxes_selector_002();
                    self.init_product_taxes_preselection_002();
                    $("#taxes_id").select2("readonly", true);
                    console.log("edit-page-menu 003")
                }
            });
            
            self._super(parent, action);
        },
        disable_fields_for_edition_002: function()
        {
            $("#taxes_id").select2("readonly", true);                     
        },
        enable_fields_for_edition_002: function()
        {
            $("#taxes_id").select2("readonly", false);
        },
        init_product_taxes_edition_002: function () {
            var self = this;
            self.enable_fields_for_edition_002();
        },
        init_product_taxes_preselection_002: function () {
            console.log('init_product_taxes_preselection_002');
            var self = this;
            var product_id = $('li.js_publish_management').attr('data-id');
            rpc.query({
                route: '/selections/taxes/get_taxes_assigned',
                params: {
                    fields: ['id','name'],
                    domain: [['id','=',parseInt(product_id)]],
                }
            }).then(function (product_taxes) {
                if(product_taxes)
                {
                    var _taxes_ids = product_taxes.taxes_preselection;
                    $('#taxes_id').val(_taxes_ids);
                    $('#taxes_id').trigger('change');
                    self.preselection_tag_002(product_taxes.taxes);
                }
            });
        },
        preselection_tag_002: function(taxes){
            var self = this;
            if(taxes)
            {
                taxes.forEach(function(tax){
                    var li = $("<li class='select2-search-choice'/>");
                    var li_text = $("<div>"+String(tax.text)+"<div/>");
                    var li_a_delete = $("<a href='#' class='select2-search-choice-close' tabindex='-1' data-id='"+String(tax.id)+"' />");
                    li_a_delete.on('click', function () 
                    {
                        self.delete_preselection_tag_002(li_a_delete);
                    });
                    var option = li.append(li_text).append(li_a_delete);                    
                    $("div.product_template_taxes_edition_nice ul.select2-choices").prepend(option);
                });
            }          
        },        
        delete_preselection_tag_002: function(element){
            var tags = $("#taxes_id").val();
            var _id = element.attr("data-id");
            tags = tags.replace(_id, 0);
            tags = tags.replace(',,', ',');
            try
            {
                tags = String(tags).split(',');
                var _tags = [];
                if(tags)
                {
                   try
                   {
                    tags.forEach(function(_tag){
                        try
                        {
                            if(parseInt(_tag)>0)
                            {
                                _tags.push(parseInt(_tag));
                            }
                        }
                        catch(ex)
                        {}
                    }); 
                   }
                   catch(ex)
                   {}
                }
                tags = _tags;
                $("#taxes_id").val(_tags);
            }
            catch(ex)
            {}

            element.closest("li").remove();
            self._super(element); 
        },
        save_product_taxes_edition_002: function () {
            var self = this;
            var taxes = $("#taxes_id").val();
            self.disable_fields_for_edition_002();
            
        },
        _start_taxes_selector_002: function () {            
            var self = this;
            var taxes_id_element = $('#taxes_id');
            taxes_id_element.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: true,
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
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        rpc.query({
                            route: '/selections/taxes/search_read',
                            params: {
                                fields: ['id','name'],
                                domain: [['type_tax_use','=','sale']],
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