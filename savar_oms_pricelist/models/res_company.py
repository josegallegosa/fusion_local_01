# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _

class res_company(models.Model):
    _inherit = 'res.company' 
    operator_type_id = fields.Many2one('operator.type', string='Tipo de Operador')