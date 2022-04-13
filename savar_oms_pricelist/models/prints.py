from odoo import api, fields, models


class Prints(models.Model):
    _name = 'prints'
    _description = 'Prints'

    name = fields.Char(string='Impresiones')
    description = fields.Text(string='Descripción')

    