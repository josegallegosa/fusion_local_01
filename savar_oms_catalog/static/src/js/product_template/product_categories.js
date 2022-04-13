odoo.define('savar_oms_catalog.product_categories', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    publicWidget.Widget.include({
        init: function (parent, action)
        {
            var self = this;
            this._super(parent, action);
        },
        get_public_categories()
        {
            var self = this;
            self._rpc({
                        model: "product.public.category",
                        method: "get_ecommerce_categories",
                        args: [''],
                      }).then(function (categories) 
                      {
                        console.log("categories get_public_categories");
                        console.log(categories);
                      });
        }
    });
});