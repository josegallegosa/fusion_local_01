from odoo import api, fields, models


class Picking(models.Model):
    _name = 'picking'
    _description = 'Picking'

    name = fields.Char(string='Picking')
    description = fields.Text(string='Descripción')

    