# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class shipping_type_id(models.Model):
    _name = 'shipping.type'

    name = fields.Char(string="Nombre")

