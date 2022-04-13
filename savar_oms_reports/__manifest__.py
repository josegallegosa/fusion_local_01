# -*- coding: utf-8 -*-
{
    'name': "savar_oms_reports",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "rockscripts",
    'website': "http://www.instagram.com/rockscripts",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
                    'base', 
                    'sale', 
                    'point_of_sale',
                    'stock',
                    'fieldservice',
                    'savar_oms_catalog'
                ],
    'data': [
                'data/reports.xml',                
                'views/business_report.xml',
                'views/business_report_history.xml',
                'views/reports/report_stock_picking_transfers/base.xml',
                'views/reports/report_stock_picking_transfers/report_stock_picking_transfers.xml',
                'views/menu.xml',
            ],
}
