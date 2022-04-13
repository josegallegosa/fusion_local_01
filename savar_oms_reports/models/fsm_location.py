# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class fsm_location(models.Model):
    _inherit = 'fsm.location'
    _description = 'Ordenes de Trabajo'

    business_reports_ids = fields.Many2many(string="Informes")