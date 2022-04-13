# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api
import sys

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime
from dateutil.relativedelta import relativedelta

class business_report_history(models.Model):
    _name = 'business.report.history'
    _description = 'Historial de Reportes para Ordenes de Trabajo'

    name = fields.Char(string="Nombre")    

    date_start_scheduled_date_start = fields.Datetime(string="Fecha inicial", select=True, default=lambda self: fields.datetime.now())
    date_ends_scheduled_date_start = fields.Datetime(string="Fecha final", select=True, default=lambda self: fields.datetime.now())

    start_create_date = fields.Datetime(string="Fecha inicial", select=True, default=lambda self: fields.datetime.now())
    ends_create_date = fields.Datetime(string="Fecha final", select=True, default=lambda self: fields.datetime.now())

    display_code_merchant = fields.Boolean(string="Cod. Orden de trabajo", default=True)
    display_scheduled_date_start = fields.Boolean(string="Fecha Inicio Despacho", default=True)
    display_partner_account = fields.Boolean(string="Cuenta", default=True)
    display_partner_channel = fields.Boolean(string="Canal", default=True)
    display_service = fields.Boolean(string="Servicio", default=True)
    display_subservice = fields.Boolean(string="Subservicio", default=True)
    display_consigned_id = fields.Boolean(string="Contacto Primario", default=True)
    display_location_id = fields.Boolean(string="Ubicación", default=True)
    

    clean_form = fields.Boolean(string="Limpiar Formulario", default=True)

    location_id = fields.Many2many('fsm.location', string="Ubicación", ondelete='cascade', index=True, inverse_name="business_reports_ids")

    consigned_id = fields.One2many("res.partner", string="Nombre del consignado", inverse_name="consigned_business_reports_history_ids")
    partner_account = fields.One2many("res.partner", string="Cuenta", domain="[('is_ot_account', '=', True)]", inverse_name="account_business_reports_history_ids")
    partner_channel = fields.One2many("res.partner", string="Canal", domain="[('is_ot_channel', '=', True)]", inverse_name="channel_business_reports_history_ids")

    service_id = fields.One2many('fsm.order.service', string='Servicio', inverse_name="service_business_history_reports_ids")
    subservice_id = fields.One2many('fsm.order.service', string='Subservicio', inverse_name="subservice_business_history_reports_ids")

    timedelta_number = fields.Selection(string="Delta de la hora", default=None, selection=[      
                                                                                            ('1',int(1)),
                                                                                            ('2',int(2)),
                                                                                            ('3',int(3)),
                                                                                            ('4',int(4)),
                                                                                            ('5',int(5)),
                                                                                            ('6',int(6)),
                                                                                            ('7',int(7)),
                                                                                            ('8',int(8)),
                                                                                            ('9',int(9)),
                                                                                            ('10',int(10)),
                                                                                            ('11',int(11)),
                                                                                            ('12',int(12)),
                                                                                            ('13',int(13)),
                                                                                            ('14',int(14)),
                                                                                            ('15',int(15)),
                                                                                            ('16',int(16)),
                                                                                            ('17',int(17)),
                                                                                            ('18',int(18)),
                                                                                            ('19',int(19)),
                                                                                            ('20',int(20)),
                                                                                            ('21',int(21)),
                                                                                            ('22',int(22)),
                                                                                            ('23',int(23)),
                                                                                          ])
    timedelta_type = fields.Selection( [
                                        ('decrement', 'Restar'),
                                        ('increment', 'Sumar'),
                                    ],
                                    default='decrement',
                                    required=True,
                                    string='Tipo Delta')

    report_type = fields.Selection( [
                                        ('report_stock_picking_transfers', 'Informe transferencias de inventario'),
                                    ],
                                    default='report_stock_picking_transfers',
                                    required=True,
                                    string='Tipo reporte')
    
    total_service_amount = fields.Float(string="Monto Total de Servicios")
    fsm_order_ids = fields.Many2many('fsm.order', string='FSM Order', inverse_name="business_reports_histories_ids")


    def generate_financial_report_pdf(self):
        pass