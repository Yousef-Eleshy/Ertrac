# -*- coding: utf-8 -*-
{
    'name': "Payslip Report Single Page",

    'summary': """
        Printing Employee Payslips on a single page""",

    'description': """
        Printing Employee Payslips on a single page
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'tags__rule', 'hr_payroll_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/payslip_report_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
