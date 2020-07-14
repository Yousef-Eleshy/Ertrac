# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class acounting_report(models.Model):
    _inherit = "account.report"
    _name = "account.custom.report"

    filter_date = {'date_from': '', 'date_to': ''}
    filter_journals = True

    def _get_columns_name(self,options):
        columns = [
            {},
            {'style':'border:1px solid black;border-right:none;padding:5px;diraction:rtl'},
            {'name': _('الايداعات'),
            'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'style':'border:1px solid black;border-left:none;padding:5px;diraction:rtl'},

            {'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'name': _('المسحوبات'),
            'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'style':'border:1px solid black;border-right:none;border-left:none;padding:5px;diraction:rtl'},
            {'style':'border:1px solid black;border-left:none;padding:5px;diraction:rtl'},
            
        ] 
        
        return columns


    @api.model
    def _get_lines(self,options,line_id=None):
        lines = []
        self.setup_options(options)
        # raise ValidationError(options['journals'][0]['selected'])
        # adding the headers Columns
        lines.append(self.headers())
        payments = self.merging_lines(options)

        for payment in payments:
            lines.append(payment)


        return lines
    
    def setup_options(self,options):
        # journals
        bank_journals = []
        if options['journals']:
            for j in options['journals']:
                if j.get('type') == 'bank':
                    bank_journals.append(j)
            options['journals'] = bank_journals
        #Bank Number
        # bank_number_filter = self.env['ir.filters'].search([('model_id', '=', 'account.custom.report')])
        # options['ir_filters'].append({                
        #         'id': bank_number_filter.id,
        #         'name': bank_number_filter.name,
        #         'domain': bank_number_filter.domain,
        #         'context': bank_number_filter.context,
        #         'selected': True
        # })



    def prepare_customer_vendor_amls(self,options):
        '''
        getting  all payment and spliting them into vendors and Customer payments
        '''
        date_from = options['date']['date_from']
        date_to = options['date']['date_to']
        all_payments = self.sudo().env['account.payment']. \
            search(['&',('payment_date','>',date_from),('payment_date','<',date_to),('journal_id.type','=','bank')])
        vendor_payments = []
        customer_payments = []
        journal_names = [j['name'] for j in options['journals'] if j['selected']]


        for payment in all_payments:
            if payment.partner_type == 'supplier':
                if len(journal_names) > 0:
                    if payment.journal_id.name in journal_names:
                        # raise ValidationError(f'{payment.journal_id.name} {journal_names}')
                        vendor_payments.append(payment)
                else:
                    vendor_payments.append(payment)


            elif payment.partner_type == 'customer':
                 if len(journal_names) > 0:
                    if payment.journal_id.name in journal_names:
                        customer_payments.append(payment)
                 else:
                    customer_payments.append(payment)

        return (vendor_payments,customer_payments)

    def prepare_lines(self,options):
        '''
        making the vendors and customers payments lines
        '''
        style = 'text-align:left;border:1px solid black;border-bottom:none;\
            border-top:none;padding:5px;padding-right:7px;diraction:rtl'
        vendor_payments,customer_payments = self.prepare_customer_vendor_amls(options)
        vendor_lines = []
        customer_lines = []
        
        # preparing vendor lines
        for payment in vendor_payments:
            columns = [
            {'name': payment.amount,'style':style},
            {'name': payment.communication,'style':style},
            {'name': payment.check_number,'style':style},
            {'name': payment.permission_number,'style':style},
            {'name': payment.partner_id.name,'style':style},
            {'name':payment.payment_date,'style':style}]
            vendor_lines.append(columns)

        #preparing customer lines 
        for payment in customer_payments:
            columns = [{'name': payment.amount,'style':style},
            {'name': payment.communication,'style':style},
            {'name': payment.permission_number,'style':style},
            {'name':payment.payment_date,'style':style}]
            customer_lines.append(columns)

        return (vendor_lines,customer_lines)


    def merging_lines(self,options):
        '''
        meging vendor and customers payments
        '''
        v_lines,c_lines = self.prepare_lines(options)
        
        lines = []
        max_num_payments = 0

    #    checking wich has more line
        if len(v_lines) > len(c_lines):
            max_num_payments = len(v_lines) 
        else:
            max_num_payments = len(c_lines) 
    
    # the loop to merge columns
        for i in range(0,max_num_payments):
            columns = []
            
            if len(c_lines) > i:
                for column in c_lines[i]:
                    columns.append(column)
            else:
                for _ in range(0,4):
                    columns.append({'name':'','style':style})
            
            if len(v_lines) > i:
                for column in v_lines[i]:
                    columns.append(column)
            else:
                for _ in range(0,6):
                    style = 'text-align:left;border:1px solid black;border-bottom:none;border-top:none'
                    columns.append({'name':'','style':style})
            
            lines.append({
                'id':'line',
                'columns':columns
            })

    
        return lines
            
            

    def headers(self):
        style = 'text-align:left;font-weight:bold;border:1px solid black;padding:5px;padding-right:7px;diraction:rtl'
        columns = [
            {'name': 'المبلغ','style':style},
            {'name': 'البيان','style':style},
            {'name': 'رقم اذن التوريد','style':style},
            {'name':'التاريخ الايداع','style':style},
            {'name': 'المبلغ','style':style},
            {'name': 'البيان','style':style},
            {'name': 'رقم الشيك','style':style},
            {'name': 'رقم اذن التوريد','style':style},
            {'name': 'اسم المستفيد','style':style},
            {'name':'التاريخ','style':style}
        ]

        return {
            'id':'header',
            'columns':columns
        }

    def _get_report_name(self):
        return _('كشف حساب بنك')
