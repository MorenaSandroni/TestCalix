# -*- coding: utf-8 -*-

{
    'name': "Technical Test",
    'description': """
        Technical Test Calix.
    """,
    'author': "Morena Sandroni",
    'version': "15.0.0.1",
    'category': "account",
    'depends': [
        'sale','account','stock','report_xlsx','sale_stock'
     ],
    'license': "GPL-3",
    'data': [
        'data/ir_sequence.xml',
        "security/ir.model.access.csv",
        'views/credit_group.xml',
        'views/res_partner.xml',
        'views/sale_channel.xml',
        'views/sale_order.xml',
        'wizards/credit_group_report_wizard.xml',
        
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
