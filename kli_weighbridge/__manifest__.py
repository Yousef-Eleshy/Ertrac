# -*- coding: utf-8 -*-
######################################################################################################
#
#   Odoo, Open Source Management Solution
#   Copyright (C) 2018  Konsaltén Indonesia (Consult10 Indonesia) <www.consult10indonesia.com>
#   @author Hendra Saputra <hendrasaputra0501@gmail.com>
#   For more details, check COPYRIGHT and LICENSE files
#
######################################################################################################

{
    'name': 'KLI Weightbridge Data Converter',
    'depends': ['base','stock','kli_purchase','sale', 'c10i_account_invoice_advance'],
    'description': """
        Special Tools to collect data from Sampit Weightbridge 
        and convert it into Odoo's Data Structure
    """,
    'author'    : "Konsaltén Indonesia (Consult10 Indonesia)",
    'website'   : "www.consult10indonesia.com",
    'category'  : 'Accounting',
    'sequence'  : 32,
    'license'   : 'AGPL-3',
    'data': [
        'data/weighbridge_data.xml',
        'security/weighbridge_security.xml',
        'security/ir.model.access.csv',
        'views/master_data_views.xml',
        'views/weighbridge_metro_views.xml',
        'views/weighbridge_import_data_views.xml',
        'views/invoice_tbs_views.xml',
        # 'report/report_views.xml',
        # 'wizard/wizard_weighbridge_recap_views.xml',
    ],
    'installable': True,
    'application': False,
}
