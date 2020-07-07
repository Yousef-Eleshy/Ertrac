# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


class YousefReport(models.AbstractModel):
    _name = 'report.yousef_report.yreport'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, task_ids):
        report_name = "Yousef Report"
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name[:31])
        
        worksheet.write('A1', 123)
