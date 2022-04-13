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
        'base',
        'account',
        'l10n_pe',
        'stock',
        'fieldservice',
    ],

    'data': [
        'data/res.zone.type.csv',
        'data/l10n_pe.res.city.district.csv',
        'views/l10n_pe_district_views.xml',
        'views/fsm_order_service_views.xml',
        'views/menuitem_views.xml',
        'security/ir.model.access.csv',
    ],

    'images': ['static/description/banner.png'],

    'application': True,
    'installable': True,
    'auto_install': False,
    "sequence": 1,
}
