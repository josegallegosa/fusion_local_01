from odoo import api, fields, models


class Optical(models.Model):
    _name = 'evaluation.optical'
    _description = 'Evaluaciones Opticas'

    full_name = fields.Char(string='Apellidos y nombres')
    
