# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FSMLocationPerson(models.Model):
    _inherit = "fsm.location.person"
    
    location_id = fields.Many2one("fsm.location", string="Location", required=True, index=True, domain="[('distrito_id', '!=', False)]")