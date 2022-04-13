# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FSMEquipment(models.Model):
    _inherit = "fsm.equipment"

    location_id = fields.Many2one("fsm.location", string="Assigned Location", domain="[('distrito_id', '!=', False)]")
    
