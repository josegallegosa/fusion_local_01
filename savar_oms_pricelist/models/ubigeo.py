from odoo import api, fields, models


class Ubigeo(models.Model):
    _name = 'ubigeo'
    _description = 'Ubigeo'

    name = fields.Char(string='Ubigeo')
    description = fields.Text(string='Descripción')

    