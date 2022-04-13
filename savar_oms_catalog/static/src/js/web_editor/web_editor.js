odoo.define('savar_oms_catalog.web_editor', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var wUtils = require('website.utils');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.Widget.include({
        init: function (parent, action) 
        {
            var self = this;
            
            $('.o_new_content_element a').on('click', function () 
            {
                self.init_add_wizard($(this).attr('data-action'));
            });
            
            $('nav.merchant_navigation_nav li#edit-page-menu').on('click', function () 
            {
                if(String( $("#edition_mode").val() ) == String("order"))
                {console.log("edit-page-menu 001")}
                else
                {
                    self.init_product_edition();
                }
                
            });
            $('nav.merchant_navigation_nav li#save-page-menu').on('click', function () 
            {
                self.save_product_edition();                
            });
            if( $('#product_detail').length>0 )
            {
                $('nav.merchant_navigation_nav').css('display','contents');
            }
            if( $("#edition_mode").length>0 )
            {
                $('nav.merchant_navigation_nav').css('display','contents');
            }
            $('nav.merchant_navigation_nav li#new-content-menu').on('click', function (event) 
            {
                if(String( $("#edition_mode").val() ) == String("order"))
                {
                    event.preventDefault();
                    window.location.href = location.protocol + '//' + location.host + '/merchant/order/new'
                }
                else
                {
                    self.init_product_add();
                }
                
            });
            this._super(parent, action);
        },
        save_product_edition: function () 
        {
            $("nav.merchant_navigation_nav li#save-page-menu").hide();
            $("nav.merchant_navigation_nav li#edit-page-menu").fadeIn();
            //hide unwished elements
            $("div.css_quantity").fadeIn();
            $("a#add_to_cart").removeClass('hide-required');
            $("a#add_to_cart").fadeIn();
            $("div#product_option_block").fadeIn();
        },
        init_product_edition: function () 
        {
            $("nav.merchant_navigation_nav li#edit-page-menu").hide();
            $("nav.merchant_navigation_nav li#save-page-menu").fadeIn();
            //hide unwished elements
            $("div.css_quantity").hide();
            $("a#add_to_cart").addClass('hide-required');
            $("div#product_option_block").hide();          
        },
        init_product_add: function () 
        {
            $("nav.merchant_navigation_nav #o_new_content_menu_choices").removeClass("o_hidden");
            $("nav.merchant_navigation_nav .o_new_content_element").css('opacity','initial');
        },
        init_add_wizard: function (_action) 
        {
            var self = this;
            if(String(_action) == "new_product")
            {
                self._createNewProduct();
            }            
        },
        _createNewProduct: function () {
            var self = this;
            return wUtils.prompt({
                id: "editor_new_product",
                window_title: _t("New Product"),
                input: _t("Product Name"),
            }).then(function (result) {
                if (!result.val) {
                    return;
                }
                return self._rpc({
                    route: '/shop/add_product',
                    params: {
                        name: result.val,
                    },
                }).then(function (url) {
                    window.location.href = url;
                    return new Promise(function () {});
                });
            });
        },
    });
});
