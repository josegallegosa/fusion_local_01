# -*- coding: utf-8 -*-
{
    'name': "savar_personalization",

    'summary': """
        Modulo savar para personalizar savarexpress.com.pe""",

    'description': """
        Modulo savar para personalizar savarexpress.com.pe
    """,

    'author': "evolutia digital",
    'website': "http://evolutia.digital",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Theme',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
    # only loaded in demonstration mode
}