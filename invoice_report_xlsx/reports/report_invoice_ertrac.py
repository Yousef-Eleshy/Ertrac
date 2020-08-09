# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import io
import base64
import math

class TaskErtracXlsxs(models.AbstractModel):
    _name = 'report.report_invoice_ertrac.report_invoice_ertrac'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, invoice_ids):
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
        worksheet.set_column('E:F', 5)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('H:H', 5)
        worksheet.set_column('J:L', 5)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:D', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('M:M', 10)
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
        worksheet.insert_image('K1', 'myimage.png', {'image_data': image,'x_scale': 1, 'y_scale': 0.5})
        current = ''
        if invoice_ids.current :
            current = invoice_ids.current
        contract = ''
        if invoice_ids.contract :
            contract = invoice_ids.contract
        worksheet.merge_range(3, 3, 3, 4, " (%s) جاري" % current, bold_center)
        worksheet.merge_range(4, 1, 4, 6, "سكك حديد مصر - عموم هندسة السكة", bold_center)
        worksheet.merge_range(6, 0, 6, 5, "بيان مرفق بفاتورة رقم       /2020", bold_right)
        worksheet.merge_range(7, 1, 7, 6, "%s طبقا " % contract, bold_right)
        worksheet.merge_range(6, 8, 6, 11, ".................. : مبلغ الإعتماد", bold_right)
        worksheet.merge_range(7, 8, 7, 11, ".................. : رقم وتاريخ الإعتماد", bold_right)
        worksheet.merge_range(8, 8, 8, 11, ".................. : قيمة العقد", bold_right)
        header = invoice_ids.narration.splitlines()
        if header:
             worksheet.merge_range(9, 1, 9, 9, header[0], bold_center)
             worksheet.merge_range(10, 1, 10, 9, header[1], bold_center)
             worksheet.merge_range(11, 1, 11, 9, header[2], bold_center)
        
        
#         worksheet.merge_range(9, 1, 9, 9, " اسم العملية : الأعمال التي قامت بتنفيذها الشركة المصرية لتجديد و صيانة خطوط السكك الحديدية", bold_center)
#         worksheet.merge_range(10, 1, 10, 8, "أعمال الصيانة الميكانيكية ما بين        بالخط الطالع والنازل      التابع لإدارة هندسة    خلال شهر   ", bold_center)
#         worksheet.merge_range(11, 1, 11, 5, " %s %s هندسة القاهرة خلال شهر" % (fields.Date.today().strftime("%B"),
#                                                                                fields.date.today().strftime("%Y")), bold_center)
        worksheet.write(12, 0, "هندسة 207")
        worksheet.write(12, 8, "مطابع السكك الحديد 2240/1996/25000")
        
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_format_total = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFC7CE'})
        cell_format_row_wrap = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1})
        cell_section_format = workbook.add_format({'bold': False, 'align': 'right', 'valign': 'vcenter',
                                               'border': 1})
        cell_section_format.set_text_wrap()
        cell_format_row_wrap.set_text_wrap()
        cell_format_header.set_center_across()
        
        cell_format_header_wrap = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#faf200'})
        cell_format_header_wrap.set_text_wrap()
        
        worksheet.merge_range(14, 0, 15, 0, 'رقم بند العقد', cell_format_header_wrap)
        worksheet.merge_range(14, 1, 15, 1, 'بيان مفردات الأعمال', cell_format_header)
        worksheet.merge_range(14, 2, 15, 2, 'الوحدة', cell_format_header_wrap)
        worksheet.merge_range(14, 3, 15, 3, 'الكمية', cell_format_header_wrap)
        worksheet.merge_range(14, 4, 14, 5, 'الثمن بالوحدة', cell_format_header_wrap)
        worksheet.write(15, 4, 'قرش', cell_format_header_wrap)
        worksheet.write(15, 5, 'جنية', cell_format_header_wrap)
        worksheet.merge_range(14, 6, 15, 6, 'النسبة', cell_format_header_wrap)
        worksheet.merge_range(14, 7, 14, 8, 'تكاليف كل بند', cell_format_header_wrap)
        worksheet.write(15, 7, 'قرش', cell_format_header_wrap)
        worksheet.write(15, 8, 'جنية', cell_format_header_wrap)
        worksheet.merge_range(14, 9, 14, 11, 'المبلغ المصرح بدفعه', cell_format_header_wrap)
        worksheet.write(15, 9, 'قرش', cell_format_header_wrap)
        worksheet.merge_range(15, 10, 15, 11, 'جنية', cell_format_header_wrap)
        worksheet.merge_range(14, 12, 15, 12, 'ملاحظات', cell_format_header)
        row = 16
        section =0

        for idx , invoice in enumerate(invoice_ids):
            for idxx , invoice_line_ids in enumerate(invoice.invoice_line_ids):
                if not invoice_line_ids.display_type:
                    if not invoice_line_ids.product_id.default_code:
                        invoice_line_ids.product_id.default_code = ''
                    unit_tuple = math.modf(invoice_line_ids.price_unit/invoice_line_ids.rated) if invoice_line_ids.rated != 0 else (0,0)
                    subtotal_tuple = math.modf(invoice_line_ids.price_subtotal)
                    allowed_tuple = math.modf(invoice_line_ids.allowed_amount)                
                    col = 0
                    worksheet.write(row, col, invoice_line_ids.product_id.default_code , cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, invoice_line_ids.product_id.name, cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, invoice_line_ids.product_uom_id.name ,cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, invoice_line_ids.quantity , cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, int(unit_tuple[0]*100), cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, int(unit_tuple[1]), cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, "%s %s" %(invoice_line_ids.rated*100,'%'), cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, int(subtotal_tuple[0]*100), cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, int(invoice_line_ids.price_subtotal), cell_format_row_wrap)
                    col += 1
                    worksheet.write(row, col, '', cell_format_row_wrap)  
                    col += 1
                    worksheet.merge_range(row, col, row , col+1, '', cell_format_row_wrap)
                    col += 1
                    col += 1
                    disc = ''
                    if invoice_line_ids.disc:
                        disc = invoice_line_ids.disc 
                    else:
                        disc = ''
                    worksheet.write(row, col, disc ,cell_format_row)
                    col += 1
                    row += 1
                elif invoice_line_ids.display_type == 'line_section' and invoice_line_ids.name == 'خصم ضمان اعمال':
                    t1_tuple = math.modf(invoice.total_line)
                    t2_tuple = math.modf(invoice.ten_perc)
                    t3_tuple = math.modf(invoice.pure)
                    section =+ 1
                    worksheet.merge_range(row, 0,row,3, '', cell_format_row_wrap)
                    worksheet.merge_range(row, 4,row,5, 'الاجمالي', cell_format_row_wrap)
                    worksheet.write(row, 7,math.floor(t1_tuple[0]*100), cell_format_row_wrap)
                    worksheet.write(row,8,t1_tuple[1], cell_format_row_wrap)
                    worksheet.merge_range(row, 9,row,12, '', cell_format_row_wrap)

                    row +=1
                    worksheet.write(row, 0,'', cell_format_row_wrap)
                    worksheet.write(row, 1, invoice_line_ids.name, cell_format_row_wrap)
                    worksheet.merge_range(row, 2,row,4, '', cell_format_row_wrap)
                    worksheet.write(row, 6,'10%', cell_format_row_wrap)
                    worksheet.write(row, 7,math.floor(t2_tuple[0]*100), cell_format_row_wrap)
                    worksheet.write(row,8,t2_tuple[1], cell_format_row_wrap)
                    worksheet.merge_range(row, 9,row,12, '', cell_format_row_wrap)
                    
                    row +=1
                    worksheet.merge_range(row, 0,row,3, '', cell_format_row_wrap)
                    worksheet.merge_range(row, 4, row, 5, 'الصافي', cell_format_row_wrap)
                    worksheet.write(row, 7,math.floor(t3_tuple[0]*100), cell_format_row_wrap)
                    worksheet.write(row,8,t3_tuple[1], cell_format_row_wrap)
                    worksheet.merge_range(row, 9,row,12, '', cell_format_row_wrap)
                    row += 1
                    
                else:
                    worksheet.merge_range(row, 0,row,12, invoice_line_ids.name , cell_section_format)
                    row += 1
            
            worksheet.merge_range(row,7, row, 8, invoice.total_machine_rent ,cell_format_row)
            row +=1
            worksheet.merge_range(row, 3, row, 5, "صافي المستخلص",cell_format_row_wrap)
            worksheet.merge_range(row,7, row, 8, invoice.pure_amount ,cell_format_row)
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
        worksheet.merge_range(row, 2, row, 8, "جميع الأعمال تمت طبقا للأصول الفنية للهيئة وبحالة جيدة", bold_center)
        row += 1
        worksheet.write(row, 1, "مندوب الشركه", bold_center)
        row += 1
        worksheet.merge_range(row-1, 7, row-1, 11, "مندوب الهيئه", bold_center)

        row += 4
        worksheet.merge_range(row, 2, row, 6, "يعتمد / ", bold_center)
        row += 1
        worksheet.merge_range(row, 2, row, 6,"رئيس مجلس الاداره والعضو المنتدب ", bold_center)
        row += 1
        worksheet.merge_range(row, 2, row, 6,"مهندس / مصطفى عبداللطيف أبوالمكارم ", bold_center)
