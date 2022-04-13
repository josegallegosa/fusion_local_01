odoo.define('savar_oms_catalog.profile', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var rpc = require('web.rpc');

    publicWidget.Widget.include({
        init: function (parent, action) {
            var self = this;
            $('#merchant_catalog_owner_01').on('click', function () {
                self._onUpdateSwitch_merchant_catalog_owner_01();
            });
            self.get_partner_merchant();
            this._super(parent, action);
        },
        _onUpdateSwitch_merchant_catalog_owner_01: function () {
            var self = this;
            try {
                var merchant_catalog_owner_01 = $('#merchant_catalog_owner_01').val();                
                if (String(merchant_catalog_owner_01) == String("True")) {
                    $('#merchant_catalog_owner_01').prop('checked', false);
                    $('#merchant_catalog_owner_01').val("False");
                } else {
                    $('#merchant_catalog_owner_01').prop('checked', true);
                    $('#merchant_catalog_owner_01').val("True");
                }
                self.set_partner_merchant(merchant_catalog_owner_01);
            }
            catch (e) {
                console.log(e);
            }
        },
        set_partner_merchant: function (is_merchant) {
            var _id = $("#partner_id").val();
            rpc.query({
                model: "res.partner",
                method: "set_partner_merchant",
                args: ["", { 'id': _id, 'is_merchant': is_merchant }],
            }).then((result) => {

            });
        },
        get_partner_merchant: function () {
            var _id = $("#partner_id").val();
            rpc.query({
                model: "res.partner",
                method: "get_partner_merchant",
                args: ["", { 'id': _id }],
            }).then((partner) => {
                try {
                    if (String(partner['merchant_catalog_owner']) == String("false")) {
                        $('#merchant_catalog_owner_01').prop('checked', false);
                        $('#merchant_catalog_owner_01').val("False");
                    } else {
                        $('#merchant_catalog_owner_01').prop('checked', true);
                        $('#merchant_catalog_owner_01').val("True");
                    }
                }
                catch (e) { }
            });
        }
    });
});