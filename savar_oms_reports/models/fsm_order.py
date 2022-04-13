# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class fsm_order(models.Model):
    _inherit = 'fsm.order'
    _description = 'Ordenes de Trabajo'

    business_reports_ids = fields.One2many('business.reports', string="Informes", inverse_name="fsm_order_id")
    business_reports_histories_ids = fields.One2many('business.report.history', string="Informes", inverse_name="fsm_order_ids")