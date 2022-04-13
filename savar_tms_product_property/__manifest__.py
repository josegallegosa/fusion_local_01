{
    'name': """
	Savar TMS Properties
    """,

    'summary': """
    """,

    'description': """
    """,

    'category': 'Warehouse',
    'version': '14.0',

    'depends': [
        'stock',
    ],

    'data': [
        'views/product_property_views.xml',
        'views/menu_item_views.xml',
        'security/ir.model.access.csv',
    ],
    
    'images': ['static/description/banner.png'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
