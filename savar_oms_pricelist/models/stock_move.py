from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    lst_price = fields.Float(string='Precio Unit',related='product_id.lst_price')
    package_lump = fields.Char(string="Bulto")
    tree2visibility = fields.Boolean(string='Visibilidad', default=True)
