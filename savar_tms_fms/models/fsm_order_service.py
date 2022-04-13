from odoo import models, fields, api, _

class FsmOrderService(models.Model):
    _name = 'fsm.order.service'
    
    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('fsm.order.service', string='Parent Service')