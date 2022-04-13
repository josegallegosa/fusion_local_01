from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.template'

    provider_owner_id = fields.Many2one('res.partner', string='Owner')
