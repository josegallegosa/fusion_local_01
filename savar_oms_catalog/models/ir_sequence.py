
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class ir_sequence(models.Model):
    _inherit = 'ir.sequence'

    def get_merchant_sequence(self, code):
        ir_sequence = request.env['ir.sequence'].next_by_code(code)
        return ir_sequence