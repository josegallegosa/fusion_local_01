from odoo import api, fields, models


class BackOffice(models.Model):
    _name = 'back.office'
    _description = 'Back Office'

    name = fields.Char(string='Back Office')
    description = fields.Text(string='Descripción')

    