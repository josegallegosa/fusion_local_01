from odoo import api, fields, models


class Storage(models.Model):
    _name = 'storage'
    _description = 'Almacenaje'

    name = fields.Char(string='Almacenaje')
    description = fields.Text(string='Descripción')

    