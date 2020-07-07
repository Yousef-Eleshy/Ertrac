
import xlsxwriter
from odoo import models, fields, api, _

class etrac_first_report(models.AbstractModel):
    _name = 'report.etrac_report_xlsx.firstreport'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data):
        report_name = "إتقرير حصر الموظفين "
        # One sheet by partner
        #workbook   = xlsxwriter.Workbook('report_employees.xlsx')
        #format1= workbook.add_format({'font size':14,'bold':True})
        #sheet1 = workbook.add_worksheet('تقرير حصر الموظفين')
        #sheet1.write(2,2,'Name',format1)