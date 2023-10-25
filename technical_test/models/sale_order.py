# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    sale_channel_id = fields.Many2one('sale.channel', string='Canal de Venta', required=True)
    credit = fields.Selection([
        ('no_limit', 'Sin límite de crédito'),
        ('available', 'Crédito Disponible'),
        ('blocked', 'Crédito bloqueado'),
        
    ], string='Credito', default='no_limit', compute='_compute_credit', store=True, readonly=True)

    @api.onchange('sale_channel_id')
    def _onchange_sale_channel_id(self):
        if self.sale_channel_id:
            self.warehouse_id = self.sale_channel_id.warehouse_id.id
    
    @api.depends('sale_channel_id','partner_id','amount_total')
    def _compute_credit(self):
        for rec in self:
            if rec.partner_id.credit_control:
                credit_group_ids = rec.partner_id.credit_group_ids.filtered(lambda group: group.sale_channel_id == rec.sale_channel_id)
                if credit_group_ids:
                    total_sales = rec.amount_total
                    company_currency = rec.company_id.currency_id
                    if rec.currency_id != company_currency:
                        total_sales = rec.currency_id._convert(total_sales, company_currency, rec.company_id, rec.date_order or fields.Date.today())
                    
                    if total_sales <= credit_group_ids[0].credit_available: # Me tomo de atrevimiento tomar el primero que aparezca, ya que en los grupos de credito no hay una limitacion de repeticion de canales de venta
                        rec.credit = 'available'
                        return
                    rec.credit = 'blocked'
                else:
                    rec.credit = 'no_limit'
            else:
                rec.credit = 'no_limit'
            
    
    def action_confirm(self):
        if self.credit == 'blocked':
            raise UserError(_('No se puede confirmar la orden de venta, el cliente tiene el crédito bloqueado'))
        return super(SaleOrder, self).action_confirm()
    
    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        res['sale_channel_id'] = self.sale_channel_id.id
        _logger.warning("entre")
        _logger.warning(self)
        _logger.warning(self.sale_channel_id)

        

        return res
