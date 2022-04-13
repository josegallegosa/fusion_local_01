from odoo import api, fields, models

class notificator_configurator(models.Model):
    _name = "notificator.configurator"

    name = fields.Char(string="Nombre")
    
    _models_001 = fields.Many2many('ir.model', string="Modelos")
    _fields_001 = fields.Many2many('ir.model.fields', string="Campos")
    _stages_ids = fields.Many2one('fsm.stage', string="Etapas")