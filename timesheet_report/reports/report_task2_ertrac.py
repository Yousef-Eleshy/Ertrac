# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class TaskErtracXlsxs(models.AbstractModel):
    _name = 'report.report_timesheet_ertrac.report_task2_ertrac'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, task_ids):
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
        bold.set_font_size(16)
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_center.set_font_size(16)
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        bold_right.set_font_size(16)
        worksheet.merge_range(3, 1, 3, 4, "محضر حصر أعمال", bold_center)
        worksheet.merge_range(4, 1, 4, 4, "الأعمال التي قامت بتنفيذها الشركة المصرية لتجديد و صيانة خطوط السكك الحديدية", bold_center)
        worksheet.merge_range(5, 1, 5, 4, "أعمال الصيانة الميكانيكية ما بين        بالخط الطالع والنازل      التابع لإدارة هندسة    خلال شهر   ", bold_center)
        worksheet.merge_range(6, 1, 6, 2, "اليوم %s" % fields.Date.today(), bold)
        worksheet.merge_range(6, 3, 6, 4, "إجتمعنا نحن كلا من :")
        worksheet.write(7, 0, "-1")
        worksheet.merge_range(7, 1, 7, 2, "السيد المهندس/ ")
        worksheet.merge_range(7, 3, 7, 4, "رئيس قسم صيانة هندسة السكة")
        worksheet.write(8, 0, "-2")
        worksheet.merge_range(8, 1, 8, 2, "السيد المهندس/ ")
        worksheet.merge_range(8, 3, 8, 4, "هندسة منطقة")
        worksheet.write(8, 0, "-3")
        worksheet.merge_range(9, 1, 9, 2, " السيــد/")
        worksheet.merge_range(9, 3, 9, 4, "مندوب الشركة المصرية")
        worksheet.merge_range(10, 1, 10, 6, "وبالمرور والمعاينة على الطبيعة تبين ان الشركة قامت بأعمال الصيانة الميكانيكية ما بين    بالخطين الطالع والنازل ", bold_center)
        worksheet.merge_range(11, 1, 11, 6, "بقسم هندسة    التابع لإدارة هندسة   :")
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_total = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFC7CE'})
        cell_format_total2 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#C6EFCE'})
        cell_format_header.set_center_across()
        
        worksheet.merge_range(13, 0, 14, 0, '')
        worksheet.merge_range(13, 1, 14, 1, 'بيان الأعمال', cell_format_header)
        worksheet.merge_range(13, 2, 14, 2, 'من كم', cell_format_header)
        worksheet.merge_range(13, 3, 14, 3, 'إلى كم', cell_format_header)
        worksheet.merge_range(13, 4, 14, 4, 'بطول', cell_format_header)
        row = 14
        tasks_arranged_increase = []
        tasks_arranged_decrease = []

        for idx , task in enumerate(task_ids):
            for idxx , timesheet_ids in enumerate(task.timesheet_ids):
                    if timesheet_ids.line_type == 'increase_line' :
                          tasks_arranged_increase.append(timesheet_ids)
                        
        for idx , task in enumerate(task_ids):
            for idxx , timesheet_ids in enumerate(task.timesheet_ids):
                    if timesheet_ids.line_type == 'decrease_line' :
                          tasks_arranged_decrease.append(timesheet_ids)
                                
        row_initial = row   
        for idxx, timesheet_ids in enumerate(tasks_arranged_increase):
                row += 1
                col = 0
                worksheet.write(row, col, '')
                col += 1
                #worksheet.write(row, col, 'الخط الطالع', cell_format_row)
                col += 1
                worksheet.write(row, col, timesheet_ids.from_km, cell_format_row)
                col += 1
                worksheet.write(row, col, timesheet_ids.to_km, cell_format_row)
                col += 1
                worksheet.write(row, col, timesheet_ids.total_km, cell_format_row)
        worksheet.merge_range(row_initial+1, 1, row , 1, 'الخط الطالع',cell_format_row)
        # Final Total
        row += 1
        col = 0
        worksheet.write(row, col, '')
        col += 1
        worksheet.write(row, col, 'إجمالي الخط الطالع', cell_format_total)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total)
        col += 1
        worksheet.write(row, col, sum(c.total_km for c in tasks_arranged_increase), cell_format_total)
        row_initial2 = row   
        for idxx, timesheet_ids in enumerate(tasks_arranged_decrease):
                row += 1
                col = 0
                worksheet.write(row, col, '')
                col += 1
                #worksheet.write(row, col, 'الخط النازل', cell_format_row)
                col += 1
                worksheet.write(row, col, timesheet_ids.from_km, cell_format_row)
                col += 1
                worksheet.write(row, col, timesheet_ids.to_km, cell_format_row)
                col += 1
                worksheet.write(row, col, timesheet_ids.total_km, cell_format_row)
        worksheet.merge_range(row_initial2+1, 1, row , 1, 'الخط النازل',cell_format_row)
        # Final Total
        row += 1
        col = 0
        worksheet.write(row, col, '')
        col += 1
        worksheet.write(row, col, ' إجمالي الخط النازل', cell_format_total)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total)
        col += 1
        worksheet.write(row, col, sum(c.total_km for c in tasks_arranged_decrease), cell_format_total)
        tasks_total = tasks_arranged_decrease + tasks_arranged_increase
        # Final Total
        row += 1
        col = 0
        worksheet.write(row, col, '')
        col += 1
        worksheet.write(row, col, 'الإجمالي', cell_format_total2)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total2)
        col += 1
        worksheet.write(row, col, '' ,cell_format_total2)
        col += 1
        worksheet.write(row, col, sum(c.total_km for c in tasks_total), cell_format_total2)
        #line total
        worksheet.merge_range(row, 4, row , 8, "بإجمالي مسافة طالع , نازل = %s  كم" % sum(c.total_km for c in tasks_total) , bold_center)
        # Lines user will write in
        row += 4
        # Footer
        row += 2
        worksheet.merge_range(row, 2, row, 6, "جميع الأعمال تمت طبقا للأصول الفنية للهيئة وبحالة جيدة", bold_center)
        row += 1
        worksheet.merge_range(row, 3, row, 5, "وتحرر هذا المحضر منا بذلك", bold_center)
        row += 1
        worksheet.write(row, 1, "مندوب الشركه", bold_center)
        row += 1
        worksheet.merge_range(row-1, 4, row-1, 5, "مندوب الهيئه", bold_center)

        row += 4
        worksheet.merge_range(row, 1, row, 6, "يعتمد / ", bold_center)
        row += 1
        worksheet.merge_range(row, 1, row, 6,"رئيس مجلس الاداره والعضو المنتدب ", bold_center)
        row += 1
        worksheet.merge_range(row, 1, row, 6,"مهندس / مصطفى عبداللطيف أبوالمكارم ", bold_center)
