from odoo import api, fields, models


class FsmStageStatus(models.Model):
    _inherit = "fsm.stage.status"

    stage_id = fields.Many2one("fsm.stage", string="Estado", domain="[('stage_type', '=', 'order')]")