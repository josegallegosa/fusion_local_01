from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class account_taxes(models.Model):
    _inherit = 'account.tax'

    def get_account_taxes_for_sale(self):
        sale_taxes = self.env['account.tax'].search([('type','=','sale')])
        return sale_taxes