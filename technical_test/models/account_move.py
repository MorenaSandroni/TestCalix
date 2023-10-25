# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"
    
    sale_channel_id = fields.Many2one('sale.channel', string='Canal de Venta')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        check_company=True, domain="[('id', 'in', suitable_journal_ids)]",
        default=lambda self: self.sale_channel_id.journal_id.id if self.sale_channel_id else None)
