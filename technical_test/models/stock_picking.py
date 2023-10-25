# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    sale_channel_id = fields.Many2one('sale.channel', string='Canal de Venta', related='sale_id.sale_channel_id', store=True)
