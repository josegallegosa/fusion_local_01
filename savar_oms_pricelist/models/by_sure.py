from odoo import api, fields, models


class BySure(models.Model):
    _name = 'by.sure'
    _description = 'Por Seguro'

    name = fields.Char(string='Por Seguro')
    description = fields.Text(string='Descripción')

    