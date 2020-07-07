# -*- coding: utf-8 -*-
{
    'name': "etrac_report_xlsx",

    'summary': """
       Etrac report xlsx 
       """,

    'description': """
    Etrac report xlsx 
    """,

    'author': "Egymentors, Muhammed Ashraf",
    'website': "https://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base','report_xlsx','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'reports/report.xml',
    ], 
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
