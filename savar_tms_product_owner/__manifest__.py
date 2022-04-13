{
    'name': """
	Savar TMS Product Owner
    """,

    'summary': """
    """,

    'description': """
    """,

    'category': 'Warehouse',
    'version': '14.0',

    'depends': [
        'base',
        'stock',
    ],

    'data': [
        'views/product_template_views.xml',
    ],
    
    'images': ['static/description/banner.png'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
