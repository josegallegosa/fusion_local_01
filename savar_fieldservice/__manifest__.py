{
    'name': """
	    Savar TMS Field Service
    """,

    'summary': """
    """,

    'description': """
    """,

    'category': 'Warehouse',
    'version': '14.0',

    'depends': [        
                    'fieldservice',
                    'fieldservice_sale_stock',
                    'fieldservice_substatus',
                    'product',
                    'odoope_toponyms',
                    'mail',
                    'base',
                    'stock',
                    'savar_oms_pricelist',
                ],

    'data': [
                'views/fsm_stages.xml',
                'views/fsm_location.xml',
                'views/res_partner.xml',
                'views/fsm_order.xml',
                'views/fsm_stage_status.xml',
                'views/product_template.xml',
                'views/report_fsm_order.xml',
                'views/fsm_stock_move.xml',
                'views/fsm_stock_picking.xml',
                'views/package_lump.xml',
                'views/notificator_configuration.xml',                
                'data/res_partner.xml',  
                'data/fsm.stage.xml',              
                # 'data/ubigeo.xml'
            ],

    'images': ['static/description/banner.png'],

    'application': True,
    'installable': True,
    'auto_install': False,
    "sequence": 1,
}
