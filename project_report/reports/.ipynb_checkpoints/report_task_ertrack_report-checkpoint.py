# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning




class TaskErtrackXlsx(models.AbstractModel):
    _name = 'report.egymentors_ertrack_report.report_task_ertrack'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, parent_tasks):
        report_name = "محضر حصر أعمال"
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name[:31])
        format_left_to_right = workbook.add_format()
        format_left_to_right.set_reading_order(1)

        format_right_to_left = workbook.add_format()
        format_right_to_left.set_reading_order(2)
        cell_format_right = workbook.add_format()
        cell_format_right.set_align('right')

        worksheet.right_to_left()
        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:X', 20)
        bold = workbook.add_format({'bold': True})
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        worksheet.merge_range(3, 1, 3, 3, "محضر حصر أعمال", bold)
        worksheet.merge_range(4, 1, 4, 5, "الأعمال التي قامت بتنفيذها الشركة المصرية لتجديد و صيانة خطوط السكك الحديدية", bold)
        worksheet.merge_range(5, 1, 5, 8, "أعمال الصيانة الميكانيكية ما بين        بالخط الطالع والنازل      التابع لإدارة هندسة    خلال شهر   ")
        worksheet.merge_range(6, 1, 6, 2, "اليوم %s" % fields.Date.today(), bold)
        worksheet.merge_range(6, 5, 6, 6, "إجتمعنا نحن كلا من :")
        worksheet.merge_range(7, 1, 7, 2, "1-السيد المهندس/")
        worksheet.merge_range(7, 5, 7, 8, "رئيس قسم صيانة هندسة السكة ببني سويف")
        worksheet.merge_range(8, 1, 8, 2, "1-السيــد/")
        worksheet.merge_range(8, 5, 8, 8, "مندوب الشركة المصرية")
        worksheet.merge_range(9, 2, 9, 10, "وبالمرور والمعاينة على الطبيعة تبين ان الشركة قامت بأعمال الصيانة الميكانيكية ما بين    بالخطين الطالع والنازل ")
        worksheet.merge_range(10, 2, 10, 6, "بقسم هندسة    التابع لإدارة هندسة   :")
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_header.set_font_size(7)
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_row.set_font_size(7)
        cell_format_header.set_center_across()
        row = 6

        for idx, task in enumerate(parent_tasks):
            col = 0
            worksheet.merge_range(row, col, row + 1, col, 'م', cell_format_header)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'بيان الأعمال', cell_format_header)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'الوحده بالكيلو', cell_format_header)
            col += 1
            worksheet.merge_range(row, col, row + 1, col, 'الكميه', cell_format_header)
            col += 1
            if task.task_header_id:
                percentages = task.task_header_id.line_ids.mapped('percent')
                last_col = col + len(percentages)
                last_col = 17
                # Total Col
                worksheet.merge_range(row, last_col, row + 1, last_col, ' النسب  السابقة المنصرفة',
                                      cell_format_header)
                worksheet.merge_range(row, last_col+1, row + 1, last_col+1, 'النسب المستجدة',
                                      cell_format_header)
                worksheet.merge_range(row, last_col+2, row + 1, last_col+2, 'إجمالى النسبة المستحقة الصرف',
                                      cell_format_header)
                # Headers Part
                worksheet.merge_range(row, col, row, col + len(percentages) - 1,
                                      'النسب المئويه لبنود الأعمال طبقا" للعقد رقم 1 لسنة 2018/2017 للتجديد بأحواش المحطات'
                                      , cell_format_header)
                row += 1
                worksheet.merge_range(row, col ,row ,last_col,'')
                for y, line in enumerate(task.task_header_id.line_ids):
                    worksheet.write(row, col+y, "%s %s%s" % (line.name, line.percent, "%")
                                    , cell_format_header)
                row += 1
                # Main Task Name Line
                worksheet.write(row, 0, idx+1, cell_format_header)
                worksheet.write(row, 1, task.name, cell_format_header)
                worksheet.merge_range(row, 2, row, col + len(percentages) + 2,
                                      ' ', cell_format_header)
                worksheet.merge_range(row, col ,row ,last_col,'', cell_format_header)

                # Sub Tasks Lines
                for idxx, child_task in enumerate(task.child_ids):
                    row += 1
                    col = 0
                    worksheet.write(row, col, '#', cell_format_row)
                    col += 1
                    worksheet.write(row, col, child_task.name, cell_format_row)
                    col += 1
                    worksheet.write(row, col, "كم", cell_format_row)
                    col += 1
                    worksheet.write(row, col, child_task.effective_hours, cell_format_row)
                    col += 1
                    for p, percent in enumerate(percentages):
                        worksheet.write(row, col, percent, cell_format_row)
                        col += 1
                        # Total Col

                    worksheet.write(row, last_col, "%s%s" % (task.task_header_id.previous, "%"),
                                    cell_format_row)
                    col += 1
                    worksheet.write(row, last_col+1, "%s%s" % (task.task_header_id.new, "%"),
                                    cell_format_row)
                    col += 1
                    worksheet.write(row, last_col+2, "%s%s" % (task.task_header_id.total, "%"),
                                    cell_format_row)
                    worksheet.merge_range(row, col ,row ,last_col,'', cell_format_row)
            else:
                raise Warning(_("Task Header Is missing"))
            # Final Total
            row += 1
            col = 0
            worksheet.write(row, col, '#', cell_format_row)
            col += 1
            worksheet.write(row, col, 'أﻷجمالى', cell_format_row)
            col += 1
            worksheet.write(row, col, 'كم', cell_format_row)
            col += 1
            worksheet.write(row, col, sum(c.effective_hours for c in task.child_ids), cell_format_row)
            worksheet.merge_range(row, col ,row ,last_col,'', cell_format_row)
            row += 1
        # Footer
        row += 2
        worksheet.write(row, 1, "مندوب الشركه", bold_center)
        worksheet.merge_range(row-1, 4, row-1, 5, "مندوب الهيئه", bold_center)

        row += 4
        worksheet.write(row, 1, "يعتمد / ", bold_right)
        row += 1
        worksheet.write(row, 1, "رئيس مجلس الاداره والعضو المنتدب ", bold_right)
        row += 1
        worksheet.write(row, 1, "مهندس / مصطفى عبداللطيف أبوالمكارم ", bold_right)
