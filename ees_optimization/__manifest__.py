# -*- coding: utf-8 -*-
{
    'name': "EES Optimization",
    'summary': """
        EES Optimization
    """,
    'description': """
        EES Optimization
    """,
    'author': "Kalim Shaikh",
    'website': "kalim",
    'category': 'Inventory/Inventory',
    'version': '1.0.0',

    'depends': [
        'stock',
        'delivery',
        'stock_picking_batch',
    ],

    'data': [
        'views/view_stock_picking_batch.xml',
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False
}
