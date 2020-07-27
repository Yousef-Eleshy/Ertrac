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

        worksheet.merge_range(4, 1, 4, 3, " %s %s بيان موقف الأعمال التى قامت بها الشركة المصرية عن شهر" % (fields.Date.today().strftime("%B"),
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
        worksheet.write(5, 2, 'ما تم خلال الشهر (عادية)', cell_format_header)
        worksheet.write(5, 3, 'ما تم خلال الشهر (نائية)', cell_format_header)
        worksheet.write(5, 4, 'اجمالى ما تم خلال الشهر', cell_format_header)

        row = 6

        for idx , timesheet in enumerate(timesheet_ids):
            task_name = timesheet.task_id.name
            worksheet.merge_range(row, 1, row, 4, task_name, bold_right)
            row += 1
            total_normal = 0.0
            total_remote = 0.0
            total_total = 0.0
            for idxx , timesheets in enumerate(timesheet_ids):
                if task_name == timesheets.task_id.name:
                    worksheet.write(row, 1, timesheets.project_id.name , cell_format_row)
                    if timesheets.region == 'normal':
                        total_normal = timesheets.unit_amount + total_normal
                        worksheet.write(row, 3, '0.000' , cell_format_row)
                        worksheet.write(row, 2, timesheets.unit_amount , cell_format_row)
                    elif timesheets.region == 'remote' :
                        total_remote = timesheets.unit_amount + total_remote
                        worksheet.write(row, 3, timesheets.unit_amount , cell_format_row)
                        worksheet.write(row, 2, '0.000' , cell_format_row)
                    total = worksheet.cell(row,3).value + worksheet.cell(row,2).value
                    total_total = total_total + total
                    worksheet.write(row, 4, total , cell_format_row)
                    row += 1
            
            # Final Total
            row += 1
            worksheet.write(row, 1, 'إجمالى (كم)')
            worksheet.write(row, 2, total_normal , cell_format_total)
            worksheet.write(row, 3, total_remote ,cell_format_total)
            worksheet.write(row, 4, total_total ,cell_format_total)