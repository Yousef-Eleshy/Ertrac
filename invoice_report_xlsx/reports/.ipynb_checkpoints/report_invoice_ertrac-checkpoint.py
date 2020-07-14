# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import io
import base64

class TaskErtracXlsxs(models.AbstractModel):
    _name = 'report.report_invoice_ertrac.report_invoice_ertrac'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, task_ids):
        report_name = "مستخلص"
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
        bold.set_font_size(14)
        bold_center = workbook.add_format({'bold': True, 'align': 'center'})
        bold_center.set_font_size(14)
        bold_right = workbook.add_format({'bold': True, 'align': 'right'})
        bold_right.set_font_size(14)
        
        # Company Logo
        company_logo = self.env.user.company_id.logo
        imgdata = base64.b64decode(company_logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('D1', 'myimage.png', {'image_data': image,'x_scale': 1.2, 'y_scale': 0.9})
        
        worksheet.merge_range(4, 1, 4, 4, "سكك حديد مصر - عموم هندسة السكة", bold_center)
        worksheet.merge_range(6, 0, 6, 3, "بيان مرفق بفاتورة رقم       /2020", bold_right)
        worksheet.merge_range(7, 1, 7, 4, "طبقا للعقد رقم (1) لسنة 2017/2018", bold_right)
        worksheet.merge_range(6, 6, 6, 8, ".................. : مبلغ الإعتماد", bold_right)
        worksheet.merge_range(7, 6, 7, 8, ".................. : رقم وتاريخ الإعتماد", bold_right)
        worksheet.merge_range(8, 6, 8, 8, ".................. : قيمة العقد", bold_right)
        
        worksheet.merge_range(9, 1, 9, 4, " اسم العملية : الأعمال التي قامت بتنفيذها الشركة المصرية لتجديد و صيانة خطوط السكك الحديدية", bold_center)
        worksheet.merge_range(10, 1, 10, 4, "أعمال الصيانة الميكانيكية ما بين        بالخط الطالع والنازل      التابع لإدارة هندسة    خلال شهر   ", bold_center)
        worksheet.merge_range(11, 1, 11, 2, " %s %s هندسة القاهرة خلال شهر" % (fields.Date.today().strftime("%B"),
                                                                               fields.date.today().strftime("%Y")), bold_center)
        worksheet.write(12, 0, "هندسة 207")
#         worksheet.write(12, 8, "مطابع السكك الحديد 2240//1996/25000")
        
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_total = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFC7CE'})
        cell_format_total2 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#C6EFCE'})
        cell_format_header.set_center_across()
        
        worksheet.merge_range(14, 0, 15, 0, 'رقم بند العقد')
        worksheet.merge_range(14, 1, 15, 1, 'بيان مفردات الأعمال', cell_format_header)
        worksheet.merge_range(14, 2, 15, 2, 'الوحدة', cell_format_header)
        worksheet.merge_range(14, 3, 15, 3, 'الكمية', cell_format_header)
        worksheet.merge_range(14, 4, 14, 5, 'الثمن بالوحدة', cell_format_header)
        worksheet.write(15, 4, 'قرش', cell_format_header)
        worksheet.write(15, 5, 'جنية', cell_format_header)
        worksheet.merge_range(14, 6, 15, 7, 'النسبة', cell_format_header)
        worksheet.merge_range(14, 8, 14, 9, 'تكاليف كل بند', cell_format_header)
        worksheet.write(15, 8, 'قرش', cell_format_header)
        worksheet.write(15, 9, 'جنية', cell_format_header)
        worksheet.merge_range(14, 10, 14, 11, 'المبلغ المصرح بصرفه', cell_format_header)
        worksheet.write(15, 10, 'قرش', cell_format_header)
        worksheet.write(15, 11, 'جنية', cell_format_header)
        worksheet.merge_range(14, 12, 15, 13, 'ملاحظات', cell_format_header)
        row = 16

        for idx , invoice in enumerate(invoice_ids):
            for idxx , invoice_line_ids in enumerate(invoice.invoice_line_ids):
                row += 1
                col = 0
                worksheet.write(row, col, invoice_line_ids.product_id.default_code , cell_format_row)
                col += 1
                worksheet.write(row, col, invoice_line_ids.product_id.name, cell_format_row)
                col += 1
                worksheet.write(row, col, invoice_line_ids.product_uom_id.name ,cell_format_row)
                col += 1
                worksheet.write(row, col, invoice_line_ids.quantity , cell_format_row)
                col += 1
                worksheet.write(row, col, invoice_line_ids.price_unit, cell_format_row)
                col += 1
                col += 1
                worksheet.write(row, col, invoice_line_ids.rated, cell_format_row)
                col += 1
                worksheet.write(row, col, invoice_line_ids.price_subtotal, cell_format_row)
                col += 1
                col += 1
                worksheet.write(row, col, invoice_line_ids.allowed_amount, cell_format_row)  
                col += 1
                col += 1
                worksheet.write(row, col, invoice_line_ids.disc ,cell_format_row)
                col += 1
#              worksheet.merge_range(row_initial+1, 1, row , 1, 'الخط الطالع',cell_format_row)
#              # Final Total
#              row += 1
#              col = 0
#              worksheet.write(row, col, '')
#              col += 1
#              worksheet.write(row, col, 'إجمالي الخط الطالع', cell_format_total)
#              col += 1
#              worksheet.write(row, col, '' ,cell_format_total)
#              col += 1
#              worksheet.write(row, col, '' ,cell_format_total)
#              col += 1
#              worksheet.write(row, col, sum(c.total_km for c in tasks_arranged_increase), cell_format_total)
        
        # Lines user will write in
        row += 6
        # Footer
        row += 2
        worksheet.merge_range(row, 0, row, 5, "جميع الأعمال تمت طبقا للأصول الفنية للهيئة وبحالة جيدة", bold_center)
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
