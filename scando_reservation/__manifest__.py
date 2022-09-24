# -*- coding: utf-8 -*-
{
    'name': "Scando Reservation",

    'summary': """
       Reservation Location""",

    'description': """
        Scando Reservation
        Reservation Location
    """,

    'author': "Kalim Shaikh",
    'website': "kalim",

    'category': 'Inventory',
    'version': '1.1.0',

    'depends': [
        'sale_management',
        'stock'
    ],

    'data': [
        'views/view_stock_location.xml'
    ],

    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False
}
