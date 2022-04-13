from odoo import api, fields, models


class ByWeight(models.Model):
    _name = 'by.weight'
    _description = 'Por Peso'

    name = fields.Char(string='Por Peso')
    description = fields.Text(string='Descripción')

    