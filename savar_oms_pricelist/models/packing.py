from odoo import api, fields, models


class Packing(models.Model):
    _name = 'packing'
    _description = 'Packing'

    name = fields.Char(string='Packing')
    description = fields.Text(string='Descripción')

    