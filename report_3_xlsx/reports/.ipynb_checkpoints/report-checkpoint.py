# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import io
import base64
import math

class ReportErtrac(models.AbstractModel):
    _name = 'report.report_3.report_3_ertrac'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, timesheet_ids):
        report_name = "تقرير  تقديم العمال بالتجديدات خلال شهر"
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name[:31])
        format_left_to_right = workbook.add_format()
        format_left_to_right.set_reading_order(1)

        format_right_to_left = workbook.add_format()
        format_right_to_left.set_reading_order(2)
        cell_format_right = workbook.add_format()
        cell_format_right.set_align('right')

        
        worksheet.right_to_left()
        worksheet.set_column('A:A', 2)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('C:E', 10)
        bold = workbook.add_format({'bold': True})
        bold.set_font_size(12)
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_center.set_font_size(12)
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        bold_right.set_font_size(12)
        
        previous_year = (int(fields.date.today().strftime("%Y")) - 1)
        # Company Logo
        company_logo = self.env.user.company_id.logo
        imgdata = base64.b64decode(company_logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('B1', 'myimage.png', {'image_data': image,'x_scale': 1, 'y_scale': 0.5})

        worksheet.merge_range(4, 1, 4, 6, "%s / %s طبقا لخطة الهيئة عام %s  تقرير تقدم العمل بالتجديدات خلال شهر " 
                              %(previous_year,fields.date.today().strftime("%Y"),
                                fields.Date.today().strftime("%B")),bold_center)
        
        cell_format_header = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1,})
        cell_format_header_2 = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1,})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_total = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFC7CE'})
        cell_format_row_wrap = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        
        cell_format_row_wrap.set_text_wrap()
        cell_format_header.set_center_across()
        
        cell_format_header.set_font_size(16)
        cell_format_header_2.set_font_size(12)
        
        cell_format_header_wrap = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_header_wrap.set_text_wrap()
        
        row = 6
        tasks = []
        # arrange timesheets according to tasks 
        for idx , timesheet in enumerate(timesheet_ids):
            tasks.append(timesheet.task_id.name)
        
        taskss = list(dict.fromkeys(tasks))
        
#         for task in taskss :
#             worksheet.merge_range(row , 1 , row , 5 , task , bold_right)
#             row += 1
#             worksheet.write(row, 5, 'ملاحظات', cell_format_header)
#             worksheet.write(row, 4, 'اجمالى المنفذ', cell_format_header)
#             worksheet.write(row, 3, 'المنفذ خلال الشهر', cell_format_header_2)
#             worksheet.write(row, 2, 'المقرر', cell_format_header)
#             worksheet.write(row, 1, 'موقع العمل', cell_format_header)
#             row + = 1 
#             for idx , timesheet in enumerate(timesheet_ids):
                
#                 if task == timesheet.task_id.name:
#                     timesheet.project_id.name
#                     timesheet.task_id.planned_hours
             
                 

        
        
        
