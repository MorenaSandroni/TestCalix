# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

CREDIT_GROUP_MIN = 1

class ResPartner(models.Model):
    _inherit = "res.partner"

    credit_control = fields.Boolean('Control de Credito')
    credit_group_ids = fields.Many2many('credit.group', string='Grupos de Credito')
    own_credit = fields.Float('own_credit', compute='_compute_own_credit', store=True)
    
    @api.depends('sale_order_ids','sale_order_ids.invoice_status','sale_order_ids.amount_total',
                 'invoice_ids','invoice_ids.state', 'invoice_ids.amount_residual')
    def _compute_own_credit(self):
        for rec in self:
            sale_orders = sum(rec.sale_order_ids.filtered(lambda s: s.state == 'sale' and s.invoice_status == 'to invoice').mapped('amount_total'))
            unpaid_invoices = sum(rec.invoice_ids.filtered(lambda i: i.move_type == 'out_invoice' and i.state == 'posted' and i.amount_residual > 0.0).mapped('amount_residual'))
            rec.own_credit = sale_orders + unpaid_invoices
            rec.credit_group_ids._compute_credit_utilized()

    @api.model
    def create(self, vals):
        rec = super(ResPartner, self).create(vals)
        if rec.credit_control and len(rec.credit_group_ids) < CREDIT_GROUP_MIN:
            raise UserError(_("No se pueden tener menos de %s grupos de crédito asignados") % CREDIT_GROUP_MIN)
        return rec

    def write(self, vals):
        rec = super(ResPartner, self).write(vals)
        if self.credit_control and len(self.credit_group_ids) < CREDIT_GROUP_MIN:
            raise UserError(_("No se pueden tener menos de %s grupos de crédito asignados") % CREDIT_GROUP_MIN)
        return rec