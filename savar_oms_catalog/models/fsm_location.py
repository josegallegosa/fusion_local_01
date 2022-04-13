# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class fsm_location(models.Model):
    _inherit = 'fsm.location'

    store_state_id = fields.Many2one(related="state_id", store=True)