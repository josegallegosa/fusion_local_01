# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class stock_move(models.Model):
    _inherit = 'stock.move'
    
    price_list = fields.Many2one('oms.pricelist', string='Tarifa Aplicada')
    price_list_line = fields.Many2one('oms.pricelist.item', string='Linea de Tarifa Aplicada')
    fsm_order_id = fields.Many2one("fsm.order", string="Pedido de Trabajo")