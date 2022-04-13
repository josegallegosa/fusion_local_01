# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class fsm_order_service(models.Model):
    _inherit = 'fsm.order.service'
    _description = 'Servicios de Ordenes de Trabajo'

    service_business_reports_ids = fields.Many2one('business.reports', string="Informes", inverse_name="service_id")
    subservice_business_reports_ids = fields.Many2one('business.reports', string="Informes", inverse_name="subservice_id")
    
    service_business_history_reports_ids = fields.Many2one('business.report.history', string="Informes", inverse_name="service_id")
    subservice_business_history_reports_ids = fields.Many2one('business.report.history', string="Informes", inverse_name="subservice_id")