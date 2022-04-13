from odoo import api, fields, models


class ProductSize(models.Model):
    _name = 'product.size'
    _description = 'Talla producto'

    name = fields.Char(string='Talla', required=True)
    description = fields.Text(string='Descripción')

    