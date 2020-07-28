# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import io
import base64
import math

class TaskErtracXlsxs(models.AbstractModel):
    _name = 'report.report_1_xlsx.report_1_ertrac'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, timesheet_ids):
        report_name = "موقف بيان الأعمال"
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
        worksheet.set_column('C:E', 10)
        bold = workbook.add_format({'bold': True})
        bold.set_font_size(12)
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_center.set_font_size(12)
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        bold_right.set_font_size(12)
        
        # Company Logo
        company_logo = self.env.user.company_id.logo
        imgdata = base64.b64decode(company_logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('B1', 'myimage.png', {'image_data': image,'x_scale': 1, 'y_scale': 0.5})

        worksheet.merge_range(4, 1, 4, 5, " %s %s بيان موقف الأعمال التى قامت بها الشركة المصرية عن شهر" % (fields.Date.today().strftime("%B"),
                                                                                            fields.date.today().strftime("%Y")),
                              bold_center)

        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_total = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFC7CE'})
        cell_format_row_wrap = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        
        cell_format_row_wrap.set_text_wrap()
        cell_format_header.set_center_across()
        
        cell_format_header_wrap = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_header_wrap.set_text_wrap()
        
        worksheet.write(5, 1, 'الخط', cell_format_header)
        worksheet.write(5, 2, 'ما تم خلال الشهر (عادية)', cell_format_header_wrap)
        worksheet.write(5, 3, 'ما تم خلال الشهر (نائية)', cell_format_header_wrap)
        worksheet.write(5, 4, 'اجمالى ما تم خلال الشهر', cell_format_header_wrap)

        row = 6
        
        tasks = []
        # arrange timesheets according to tasks 
        for idx , timesheet in enumerate(timesheet_ids):
            tasks.append(timesheet.task_id.name)
        
        taskss = list(dict.fromkeys(tasks))
        
        for task in taskss :
            total = 0
            total_normal = 0.0
            total_remote = 0.0
            total_total = 0.0
            worksheet.merge_range(row, 1, row, 4, task, bold_right)
            for idx , timesheet in enumerate(timesheet_ids):
                normal = 0.0
                remote = 0.0
                if task == timesheet.task_id.name:
                    worksheet.write(row, 1, timesheet.project_id.name , cell_format_row)
                    if timesheet.region == 'normal':
                        normal = timesheet.unit_amount
                        remote = 0.0
                        total_normal = timesheet.unit_amount + total_normal
                        worksheet.write(row, 3, '0.000' , cell_format_row_wrap)
                        worksheet.write(row, 2, timesheet.unit_amount , cell_format_row_wrap)
                    elif timesheet.region == 'remote' :
                        remote = timesheet.unit_amount
                        normal = 0.0
                        total_remote = timesheet.unit_amount + total_remote
                        worksheet.write(row, 3, timesheet.unit_amount , cell_format_row_wrap)
                        worksheet.write(row, 2, '0.000' , cell_format_row_wrap)
                    total = remote + normal
                    worksheet.write(row, 4, total , cell_format_row_wrap)
                    total_total = total_total + total
                    row += 1
            row += 1
            # Final Total
            worksheet.write(row, 1, 'إجمالى (كم)')
            worksheet.write(row, 2, total_normal , cell_format_total)
            worksheet.write(row, 3, total_remote ,cell_format_total)
            worksheet.write(row, 4, total_total ,cell_format_total)
