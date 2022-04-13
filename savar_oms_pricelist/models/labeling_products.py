from odoo import api, fields, models


class LabelingProducts(models.Model):
    _name = 'labeling.product'
    _description = 'Etiquetado Productos'

    name = fields.Char(string='Etiquetado Producto')
    description = fields.Text(string='Descripción')

    