from odoo import api, fields, models


class ByPickUp(models.Model):
    _name = 'by.pick.up'
    _description = 'Por Recojo'

    name = fields.Char(string='Por Recojo')
    description = fields.Text(string='Descripción')

    