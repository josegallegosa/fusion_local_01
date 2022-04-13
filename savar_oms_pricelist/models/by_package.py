from odoo import api, fields, models


class ByPackages(models.Model):
    _name = 'by.package'
    _description = 'Por Bultos'

    name = fields.Char(string='Por Bultos')
    description = fields.Text(string='Descripción')

    