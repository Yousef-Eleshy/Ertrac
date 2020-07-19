# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


# Ahmed Salama Code Start ---->


class PayslipXlsx(models.AbstractModel):
    _name = 'report.egymentors_hr.report_payslip_salary_rules'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, payslips):
        report_name = "عناصر اجر الموظفين"
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
        worksheet.set_column('C:X', 15)
        bold = workbook.add_format({'bold': True})
        worksheet.merge_range(1, 6, 1, 8, self.env.user.company_id.name)
        worksheet.merge_range(2, 4, 2, 8, self.env.user.street)
        worksheet.merge_range(3, 1, 3, 3, "%s عناصر اجر الموظفين بتاريخ" % fields.Date.today(), bold)
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#898a8c'})
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1, 'fg_color': '#D7E4BC'})
        cell_format_header.set_center_across()
        row = 6
        # Get Active Salary Rules
        salary_rules = []
        for payslip_id in payslips:
            for line in payslip_id.line_ids:
                if line.total and line.salary_rule_id.appears_on_payslip\
                        and line.salary_rule_id.id not in salary_rules:
                    salary_rules.append(line.salary_rule_id.id)
        worksheet.write(row, 0, 'م', cell_format_header)
        worksheet.write(row, 1, 'إسم الموظف', cell_format_header)
        salary_rules_obj = self.env['hr.salary.rule']
        payslip_line_obj = self.env['hr.payslip.line']
        col = 2
        for idx, rule in enumerate(salary_rules):
            rule_id = salary_rules_obj.browse(rule)
            worksheet.write(row, col, rule_id.name, cell_format_header)
            col += 1
        worksheet.write(row, col, 'حساب بنك الموظف', cell_format_header)
        row += 1
        for idx, payslip_id in enumerate(payslips):
            worksheet.write(row, 0, idx + 1, cell_format_row)
            worksheet.write(row, 1, payslip_id.employee_id.name, cell_format_row)
            col = 2
            for rule in salary_rules:
                line_id = payslip_id.line_ids.filtered(lambda l: l.salary_rule_id.id == rule)
                total = line_id and line_id.total or 0.0
                worksheet.write(row, col, total, cell_format_row)
                col += 1
            bank = payslip_id.employee_id.bank_account_id and payslip_id.employee_id.bank_account_id.acc_number or '------------'
            worksheet.write(row, col, bank, cell_format_header)
            row += 1
        worksheet.merge_range(row, 0, row, 1, 'الإجمالى', cell_format_header)
        col = 2
        for rule in salary_rules:
            total = sum(l.total for l in payslip_line_obj.search([('salary_rule_id', '=', rule),
                                                                  ('slip_id', 'in', payslips.mapped('id'))]))
            worksheet.write(row, col, total, cell_format_header)
            col += 1

            
# Ahmed Salama Code End.
