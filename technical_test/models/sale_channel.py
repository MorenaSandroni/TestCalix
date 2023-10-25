# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
import logging
_logger = logging.getLogger(__name__)

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Sale Channel'
    _inherit = ['mail.thread', 'sequence.mixin']
    
    name = fields.Char('Nombre', required=True, tracking=True)
    date = fields.Date('date')
    sequence = fields.Char('Secuencia',readonly=True, tracking=True)
    warehouse_id = fields.Many2one('stock.warehouse', 'Almacen', tracking=True)
    journal_id = fields.Many2one('account.journal', string="Diario Contable", required=True,
                                 domain=[('type', '=', 'sale')], tracking=True)
    
    @api.model
    def create(self, vals):
        if vals.get('sequence', _('/')) == _('/'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('sale.channel') or '/'
        result = super(SaleChannel, self).create(vals)
        return result