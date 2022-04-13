
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = 'res.partner'

    merchant_catalog_owner = fields.Boolean(string="Comerciante")
    is_operator = fields.Boolean(string="Operador")