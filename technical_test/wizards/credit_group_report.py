#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)



class CreditGroupReport(models.TransientModel):
    _name = 'credit.group.report'
    _description = 'Credit Group Report'

    credit_group_ids = fields.Many2many('credit.group', string='Grupos de Credito')



    def action_generate_xlsx_report(self):
        return self.env.ref('technical_test.report_credit_group_report_xlsx').report_action(self)



class CreditGroupXLSX(models.TransientModel):
    _name = 'report.credit_group_report_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Credit Group Report'



    def generate_xlsx_report(self, workbook, data, values):
        row = 5
        for obj in values:
            report_name = 'Reporte de Grupos de Credito'
            color_blue = '#8EB4E3'
            thead_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'bg_color': color_blue
                }
            )
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'}
            )
            for group in obj.credit_group_ids:
                sheet_name = "Reporte de Grupos de Credito: " + str(group.name)
                worksheet = workbook.add_worksheet(sheet_name[:31])
                bold = workbook.add_format({'bold': True})
                date_line = workbook.add_format(
                    {'border': 1, 'num_format': 'dd-mm-yyyy',
                    'align': 'center'})
                worksheet.set_column('A:A', 50)
                worksheet.set_column('B5:G5', 15)
                
                worksheet.merge_range(
                    'B1:G1', sheet_name, merge_format)
                worksheet.write('B5', 'Grupo de Credito', thead_format)
                worksheet.write('C5', group.name, merge_format)
                worksheet.write('D5', 'Codigo de Grupo', thead_format)
                worksheet.write('E5', group.code, merge_format)
                worksheet.write('F5', 'Canal de Venta', thead_format)
                worksheet.write('G5', group.sale_channel_id.name, merge_format)
                
                clients = self.env['res.partner'].search([('credit_group_ids', 'in', [group.id])])
                sale_orders = clients.sale_order_ids.filtered(lambda s: s.state == 'sale' and s.invoice_status == 'to invoice')
                invoices = clients.invoice_ids.filtered(lambda i: i.move_type == 'out_invoice' and i.state == 'posted' and i.amount_residual > 0.0)
                row = 7
                worksheet.write(row, 1, 'Clientes', thead_format)
                row += 1
                worksheet.write(row, 1, 'Nombre', thead_format)
                worksheet.write(row, 2, 'Numero de Documento', thead_format)
                worksheet.write(row, 3, 'Telefono', thead_format)
                worksheet.write(row, 4, 'Correo Electronico', thead_format)
                
                for client in clients:
                    row += 1
                    worksheet.write(row, 1, client.name, merge_format)
                    worksheet.write(row, 2, client.vat, merge_format)
                    worksheet.write(row, 3, client.mobile, merge_format)
                    worksheet.write(row, 4, client.email, merge_format)

                
                row += 2
                worksheet.write(row, 1, 'Ordenes de Venta', thead_format)
                row += 1
                worksheet.write(row, 1, 'Numero', thead_format)
                worksheet.write(row, 2, 'Fecha', thead_format)
                worksheet.write(row, 3, 'Importe Total', thead_format)
                for sale in sale_orders:
                    row += 1
                    worksheet.write(row, 1, sale.name, merge_format)
                    worksheet.write(row, 2, sale.date_order.strftime('%d/%m/%Y'), merge_format)
                    worksheet.write(row, 3, sale.amount_total, merge_format)

                row += 2
                worksheet.write(row, 1, 'Facturas de Venta', thead_format)
                row += 1
                worksheet.write(row, 1, 'Numero', thead_format)
                worksheet.write(row, 2, 'Fecha', thead_format)
                worksheet.write(row, 3, 'Importe Adeudado', thead_format)
                for inv in invoices:
                    row += 1
                    worksheet.write(row, 1, inv.name, merge_format)
                    worksheet.write(row, 2, inv.invoice_date.strftime('%d/%m/%Y'), merge_format)
                    worksheet.write(row, 3, inv.amount_residual, merge_format)

                
            workbook.close()


