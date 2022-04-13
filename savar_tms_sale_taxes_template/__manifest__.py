{
    'name': """
        NAME |
    """,

    'summary': """
        SUMMARY. |
    """,

    'description': """
        DESCRIPTION. |
    """,

    'author': 'Develogers | Ailton Salguero Bazalar',
    'website': 'https://www.linkedin.com/in/ailton-salguero',
    'support': 'ailton.salguero@gmail.com',
    'live_test_url': 'https://demo.develogers.com',
    'license': 'LGPL-3',

    'category': 'Invoice',
    'version': '1.0',
    
    'price': 9.99,
    'currency': 'EUR',

    'depends': [
        'base',
        'sale',
    ],

    'data': [
        #'security/ir.model.access.csv',
        'views/taxes_templates.xml',
    ],
    
    'images': ['static/description/banner.png'],
    
    'application': True,
    'installable': True,
    'auto_install': False,
}
