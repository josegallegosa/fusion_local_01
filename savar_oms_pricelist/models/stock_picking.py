from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    package_lump = fields.Char(string="Bulto")