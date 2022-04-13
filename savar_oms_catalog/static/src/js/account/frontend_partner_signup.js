odoo.define('savar_oms_catalog.signup', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
        selector: '#merchant_catalog_owner',
        events: {
            'click #merchant_catalog_owner': '_onUpdateSwitch_merchant_catalog_owner'
        },
        init: function (parent, action) {
            this._super(parent, action);
            $('#merchant_catalog_owner').prop('checked', false);
        },
        _onUpdateSwitch_merchant_catalog_owner: function () {
            var merchant_catalog_owner = $('#merchant_catalog_owner').val();
            if ($('#merchant_catalog_owner').is(':checked')) {
                $(this).prop('checked', true);
            } else {
                $(this).prop('checked', false);
            }
        },
    });
});