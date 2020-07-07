

from odoo import models, fields, api, _

class etrac_first_report(models.AbstractModel):
    _name = 'report.etrac_report_xlsx.firstreport'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, task_ids):
        report_name = "إتقرير حصر الموظفين "
        # One sheet by partner
        worksheet = workbook.add_worksheet('تقرير حصر الموظفين')
        