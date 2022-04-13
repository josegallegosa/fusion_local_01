
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class sale_orders_massive(models.Model):
    _name = 'sale.orders.massive'

    name = fields.Char(string="Nombre")
    file_name = fields.Char(string="Archivo")
    file_binary = fields.Binary(string="Excel")