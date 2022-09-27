# -*- coding: utf-8 -*-
{
    'name': "EES Access Right",
    'summary': """
        EES Access Right
    """,
    'description': """
        EES Access Right
    """,
    'author': "Kalim Shaikh",
    'website': "kalim",
    'category': 'Sales',
    'version': '1.2.0',

    'depends': [
        'sale_management',
    ],

    'data': [
        'security/ees_access_right_security.xml',
        'views/product_template_view.xml',
        'views/product_view.xml',
        'views/sale_order_view.xml',
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False
}
