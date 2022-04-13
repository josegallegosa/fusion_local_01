from odoo import api, fields, models

class fsm_stages(models.Model):
    _inherit = "fsm.stage"

    services = fields.Many2many('fsm.order.service', string="Servicios de Trabajo")