from odoo import api, fields, models


class PaymentType(models.Model):
    _name = 'payment.type'
    _description = 'Tipo De Pago'

    name = fields.Char(string='Tipo De Pago')
    description = fields.Text(string='Descripción')

    