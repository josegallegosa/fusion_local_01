#<!-- # BEGIN JEG -->
from odoo import api, fields, models


class TypeOrder(models.Model):
    _name = 'type.order'
    _description = 'Tipo de orden'

    name = fields.Char(string='Tipo de orden')
    description = fields.Text(string='Descripción')
#<!-- # ENDS JEG -->
    