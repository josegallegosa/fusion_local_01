# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = 'res.partner'
    _description = 'Perfiles para Ordenes de Trabajo'

    consigned_business_reports_ids = fields.Many2one('business.reports', string="Informes", inverse_name="consigned_id")
    account_business_reports_ids = fields.Many2one('business.reports', string="Informes", inverse_name="partner_account")
    channel_business_reports_ids = fields.Many2one('business.reports', string="Informes", inverse_name="partner_channel")

    consigned_business_reports_history_ids = fields.Many2one('business.reports.history', string="Informes", inverse_name="consigned_id", default=None)
    account_business_reports_history_ids = fields.Many2one('business.reports.history', string="Informes", inverse_name="partner_account", default=None)
    channel_business_reports_history_ids = fields.Many2one('business.reports.history', string="Informes", inverse_name="partner_channel", default=None)