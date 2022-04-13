from odoo import api, fields, models


class ResZoneType(models.Model):
    _name = 'res.zone.type'
    _description = 'Tipo de zona'

    name = fields.Char(string='Name')
