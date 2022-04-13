# Copyright (C) 2019 Brian McMaster
# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    fsm_location_id = fields.Many2one(
        "fsm.location",
        string="Service Location",
        help="SO Lines generating a FSM order will be for this location",
        domain="[('distrito_id', '!=', False)]"
        )