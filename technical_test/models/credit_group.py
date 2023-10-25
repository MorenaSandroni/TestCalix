# -*- coding: utf-8 -*-
from odoo import models, api, fields, _
from odoo.exceptions import UserError, ValidationError
PROHIBITED_CODE = '026'
class CreditGroup(models.Model):
    _name = 'credit.group'
    _description = 'Credit Group'
    _inherit = ['mail.thread', 'sequence.mixin']
    
    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Código', required=True, unique=True)
    sale_channel_id = fields.Many2one('sale.channel', string='Canal de Venta', required=True)
    credit_global = fields.Float(string='Crédito Global', required=True)
    credit_utilized = fields.Float(string='Crédito Utilizado', compute='_compute_credit_utilized', store=True)
    credit_available = fields.Float(string='Crédito Disponible', compute='_compute_credit_available', store=True)
    date = fields.Date('date')
    
    def _compute_credit_utilized(self):
        for group in self:
            clients = self.env['res.partner'].search([('credit_group_ids', 'in', [group.id])])
            group.credit_utilized = sum(clients.mapped('own_credit'))

    @api.depends('credit_utilized')
    def _compute_credit_available(self):
        for group in self:
            group.credit_available = group.credit_global - group.credit_utilized

    @api.model
    def create(self, vals):
        rec = super(CreditGroup, self).create(vals)
        if rec.code == PROHIBITED_CODE:
            raise UserError(_("El código %s está prohibido") % PROHIBITED_CODE)
        return rec

    def write(self, vals):
        rec = super(CreditGroup, self).write(vals)
        if self.code == PROHIBITED_CODE:
            raise UserError(_("El código %s está prohibido") % PROHIBITED_CODE)
        return rec