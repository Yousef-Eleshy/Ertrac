# -*- coding: utf-8 -*-
{
    'name': "Report 3 XLSX",

    'summary': """
        تقرير  تقديم العمال بالتجديدات خلال شهر""",

    'description': """
        تقرير  تقديم العمال بالتجديدات خلال شهر
    """,

    'author': "Egymentors",
    'website': "http://www.egymentors.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management','account','account_accountant','project','hr_timesheet','sale_timesheet','report_xlsx',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'reports/report.xml',
    ],
}
