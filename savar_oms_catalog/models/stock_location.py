# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class stock_location(models.Model):
    _inherit = 'stock.location'

    fsm_input_type = fields.Selection(string="Tipo", selection=[('dispatch','Despacho'),('in','Rebastecer')])