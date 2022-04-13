# -*- coding: utf-8 -*-
{
    'name': "savar_oms_catalog",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.instagram.com/rockscripts",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
                    'base', 
                    'account',
                    'sale',
                    'purchase',
                    'web',
                    'website', 
                    'product',
                    'stock',
                    'website_form',
                    'website_sale',
                    'web_editor',
                    'portal',
                    'website_webkul_addons',
                    'website_mega_menus',
                    'fieldservice',
                    'fieldservice_stock',
                    'savar_fieldservice'
                ],
    'data': [                
                #'data/groups.xml',
                'data/sequence.xml',
                'views/models/res_partner.xml',
                'views/models/product_template.xml',
                'views/models/sale_order.xml',
                'views/models/fsm_order.xml',
                'views/models/fsm_stock_location.xml',
                'views/models/fsm_stock_move.xml',
                'views/models/purchase_order.xml',
                'views/models/stock_picking_type.xml',
                'views/models/fsm_stock_picking.xml',
                'views/assets/frontend.xml',
                'views/assets/backend.xml',
                'views/web/web_editor.xml',                
                'views/website/signup.xml',
                'views/website/my_account.xml',
                'views/website_sale/product_template_extra_fields.xml',
                'views/website_sale/taxes.xml',
                'views/website_sale/product_template_categories.xml',
                'views/account/merchant_categories.xml',
                'views/account/pages/categories.xml',
                'views/account/merchant_orders.xml',
                'views/account/report_fsm_order.xml',
                'views/account/report_sale_order.xml',
                'views/account/pages/informe_fsm_order.xml',
                'views/account/pages/informe_sale_order.xml',
                'views/account/fsm_orders.xml',
                'views/account/pages/orders_fsm.xml',
                'views/account/pages/orders.xml',
                'views/account/merchant_new_order.xml',
                'views/account/merchant_new_order_fsm.xml',
                'views/account/pages/new_fsm_order.xml',
                'views/account/pages/new_order.xml',
                'views/account/pages/edit_order.xml',
                'views/account/pages/edit_order_form.xml',
                'views/account/pages/quotations_list.xml',
                'views/account/pages/quotations_portal_table.xml',
                'views/account/pages/orders_buttons.xml',
                'views/website_sale/massive_uploads/sale_orders_massive.xml',
                'views/models/xlsx_templates.xml'
                #'security/ir.rule.csv',
                #'security/ir.model.access.csv',
            ],
    'qweb': [
                'static/src/xml/xls_importer.xml'
            ]

}