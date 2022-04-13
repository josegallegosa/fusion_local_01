# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api
import sys

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime
from dateutil.relativedelta import relativedelta

class business_report(models.Model):
    _name = 'business.reports'
    _description = 'Ordenes de Trabajo'

    name = fields.Char(string="Nombre")
    fsm_order_id = fields.Many2many('fsm.order', string='FSM Order', inverse_name="business_reports_ids")

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

    consigned_id = fields.One2many("res.partner", string="Nombre del consignado", inverse_name="consigned_business_reports_ids")
    partner_account = fields.One2many("res.partner", string="Cuenta", domain="[('is_ot_account', '=', True)]", inverse_name="account_business_reports_ids")
    partner_channel = fields.One2many("res.partner", string="Canal", domain="[('is_ot_channel', '=', True)]", inverse_name="channel_business_reports_ids")

    service_id = fields.One2many('fsm.order.service', string='Servicio', inverse_name="service_business_reports_ids")
    subservice_id = fields.One2many('fsm.order.service', string='Subservicio', inverse_name="subservice_business_reports_ids")

    timedelta_number = fields.Selection(string="Delta de la hora", default='0', selection=[
                                                                                            ('0',int(0)),
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

    def generate_financial_report(self):
        _logger.warning("report_type report_stock_picking_transfers")
        _logger.warning(self.report_type)
        if(self.report_type == str('report_stock_picking_transfers')):
            return self.env.ref('savar_oms_reports.report_stock_picking_transfers_pdf').report_action(self)        
        self.reset_form()
    
    def reset_form(self):
        self.date_start_scheduled_date_start = fields.datetime.now()
        self.date_ends_scheduled_date_start = fields.datetime.now()        

    def get_inform_vals(self, for_history=False):
        _logger.warning("report_type get_inform_vals")
        _logger.warning(self.report_type)    

        _domain = []    
        
        date_start_scheduled_date_start = self.date_start_scheduled_date_start
        date_ends_scheduled_date_start = self.date_ends_scheduled_date_start

        start_create_date = self.start_create_date
        ends_create_date = self.ends_create_date

        if(self.timedelta_type == 'decrement'):
            try:
                if(int(self.timedelta_number)>0):
                    if(self.date_start_scheduled_date_start and self.date_ends_scheduled_date_start):
                        date_start_scheduled_date_start = (self.date_start_scheduled_date_start - relativedelta(hours=int(self.timedelta_number)))
                        date_ends_scheduled_date_start = (self.date_ends_scheduled_date_start - relativedelta(hours=int(self.timedelta_number)))

                    if(self.start_create_date and self.ends_create_date):
                        start_create_date = (self.start_create_date - relativedelta(hours=int(self.timedelta_number)))
                        ends_create_date = (self.ends_create_date - relativedelta(hours=int(self.timedelta_number)))
            except:
                pass
        else:
            try:
                if(int(self.timedelta_number)>0):
                    if(self.date_start_scheduled_date_start and self.date_ends_scheduled_date_start):
                        date_start_scheduled_date_start = (self.date_start_scheduled_date_start + relativedelta(hours=int(self.timedelta_number)))
                        date_ends_scheduled_date_start = (self.date_ends_scheduled_date_start + relativedelta(hours=int(self.timedelta_number)))
                    if(self.start_create_date and self.ends_create_date):
                        start_create_date = (self.start_create_date + relativedelta(hours=int(self.timedelta_number)))
                        ends_create_date = (self.ends_create_date + relativedelta(hours=int(self.timedelta_number)))
            except:
                pass

        vals = {                    
                    'display_partner_account':bool(self.display_partner_account),
                    'display_partner_channel':bool(self.display_partner_channel),
                    'display_service':bool(self.display_service),
                    'display_subservice':bool(self.display_subservice),
                    'display_consigned_id':bool(self.display_consigned_id),
                    'display_location_id':bool(self.display_location_id),
                    'location_ids': [],
                    'history':[],
                }
        
        if(start_create_date != ends_create_date):
            _domain.append(['create_date','>=',start_create_date])
            _domain.append(['create_date','<=',ends_create_date])
            vals['start_create_date'] = str(start_create_date).strip()
            vals['ends_create_date'] = str(str(ends_create_date).strip()).split('.')[0]
            pass

        if(date_start_scheduled_date_start != date_ends_scheduled_date_start):
            _domain.append(['date_start','>=',date_start_scheduled_date_start])
            _domain.append(['date_start','>=',date_ends_scheduled_date_start])
            vals[ 'date_start_scheduled_date_start'] = str(date_start_scheduled_date_start).strip()
            vals[ 'date_ends_scheduled_date_start'] = str(str(date_ends_scheduled_date_start).strip()).split('.')[0]
            pass
        try:
            _logger.warning("self.location_id)")
            _logger.warning(self.location_id)
            if((self.location_id)):
                _domain.append([ 'location_id', 'in', self.location_id.ids ])
                _logger.warning("_domain")
                _logger.warning(_domain)
                for location in self.location_id:
                    _logger.warning("_domain 001")
                    vals['location_ids'].append({'name':str(location.name), 'email':str(location.email)})
                    _logger.warning("_domain 001 **** ----") 
                    _logger.warning(vals)
                    _logger.warning("_domain 001 ****") 
        except Exception as e:
            exc_traceback = sys.exc_info()
            _logger.warning(getattr(e, 'message', repr(e))+" ON LINE "+format(sys.exc_info()[-1].tb_lineno)) 
        
        try:
            if((self.consigned_id)):
                _domain.append(['consigned_id', 'in', self.consigned_id.ids])
        except:
            pass
        
        try:
            if((self.partner_account)):
                _domain.append(['partner_account', 'in', self.partner_account.ids])
        except:
            pass
        
        try:
            if((self.partner_channel)):
                _domain.append(['partner_channel', 'in', self.partner_channel.ids])
        except:
            pass
        
        try:
            if(self.service_id):
                _domain.append(['service_id', 'in', self.service_id.ids])
        except:
            pass
        
        try:
            if(self.subservice_id):
                _domain.append(['subservice_id', 'in', self.subservice_id.ids])
        except:
            pass

        fsm_orders = self.env['fsm.order'].sudo().search(_domain)

        business_report_history = {
                                    'name': str(fields.datetime.now()) + str("-") + str(self.name),                                                                       
                                    'display_code_merchant': self.display_code_merchant,
                                    'display_scheduled_date_start': self.display_scheduled_date_start,
                                    'display_partner_account': self.display_partner_channel,
                                    'display_service': self.display_service,
                                    'display_subservice': self.display_subservice,
                                    'display_consigned_id': self.display_consigned_id,
                                    'display_location_id': self.display_location_id,
                                    'clean_form': self.clean_form,
                                    'location_id': self.location_id,
                                    #'timedelta_number': str("'"+str(self.timedelta_number)+"'"),
                                    'timedelta_type': self.timedelta_type,
                                    'report_type': self.report_type,                                    
                                  }    

        _logger.warning("business_report_history get_inform_by_fsm_orders_processed")
        _logger.warning(business_report_history)                              
        
        inform = self.get_inform_by_fsm_orders_processed(fsm_orders)

        _logger.warning("inform get_inform_by_fsm_orders_processed")
        _logger.warning(inform)

        if('total_service_amount' in inform):
            vals['total_service_amount'] = inform['total_service_amount']
            #business_report_history['amount_service_total'] =  float(vals['amount_service_total'])
        
        if('account_ids_service_amount' in inform):
            vals['account_ids_service_amount'] = inform['account_ids_service_amount']
        if('channel_ids_service_amount' in inform):
            vals['channel_ids_service_amount'] = inform['channel_ids_service_amount']
        if('service_ids_service_amount' in inform):
            vals['service_ids_service_amount'] = inform['service_ids_service_amount']
        if('subservice_ids_service_amount' in inform):
            vals['subservice_ids_service_amount'] = inform['subservice_ids_service_amount']

        _logger.warning("get_inform_vals OT")
        _logger.warning(_domain)
        _logger.warning(fsm_orders)

        if(fsm_orders):
            vals['fsm_orders'] = fsm_orders
            pass

        _logger.warning('get_inform_vals vals')
        _logger.warning(vals)       
        
        _business_report_history = self.env['business.report.history'].sudo().create(business_report_history)
        if(fsm_orders): 
            if(_business_report_history):
                _business_report_history.sudo().update({
                                                            'fsm_order_ids': fsm_orders,
                                                        })
        if(_business_report_history):
            if(self.service_id):
                service_ids = self.env['fsm.order.service'].sudo().search([('id','in',self.service_id.ids)])
                _business_report_history.sudo().update({
                                                            'service_id': service_ids,
                                                        })
            if(self.subservice_id):
                subservice_ids = self.env['fsm.order.service'].sudo().search([('id','in',self.subservice_id.ids)])
                _business_report_history.sudo().update({
                                                            'subservice_id': subservice_ids,
                                                        })
        _dates = {  
                    'date_start_scheduled_date_start': date_start_scheduled_date_start if date_start_scheduled_date_start!=False else None,
                    'date_ends_scheduled_date_start': date_ends_scheduled_date_start if date_ends_scheduled_date_start!=False else None,
                    'start_create_date': start_create_date if start_create_date!=False else None,
                    'ends_create_date': ends_create_date if ends_create_date!=False else None,
                 }
        _business_report_history.sudo().update(_dates)
        
            #if(self.consigned_id):
            #    _business_report_history.sudo().update({
            #                                                'consigned_id': self.consigned_id,
            #                                            })
            #if(self.partner_account):
            #    partner_account_ids = self.env['res.partner'].sudo().search([('id','in',self.partner_account.ids)])
            #    _business_report_history.sudo().update({
            #                                                'partner_account': partner_account_ids,
            #                                            })
            #if(self.partner_channel):
            #    _business_report_history.sudo().update({
            #                                                'partner_channel': self.partner_channel,
            #                                            })

        if(self.clean_form):
            self.reset_form()
        return vals

# domain=[['districto_id','!=', False]]

    def get_inform_by_fsm_orders_processed(self, fsm_orders):
        inform = {
                    'total_service_amount': float(), 
                    'account_ids_service_amount': float(),
                    'channel_ids_service_amount': float(),
                    'service_ids_service_amount': float(),
                    'subservice_ids_service_amount': float(),
                 }
        if(fsm_orders):
            if(self.partner_account):
                inform['account_ids_service_amount'] = self.get_account_ids_service_amount(fsm_orders)
            if(self.partner_channel):
                inform['channel_ids_service_amount'] = self.get_channel_ids_service_amount(fsm_orders)
            if(self.service_id):
                inform['service_ids_service_amount'] = self.get_service_ids_service_amount(fsm_orders)
            if(self.subservice_id):
                inform['subservice_ids_service_amount'] = self.get_subservice_ids_service_amount(fsm_orders)    
            for fsm_order in fsm_orders:
                inform['total_service_amount'] += float(fsm_order.service_amount)
        return inform
    
    def get_account_ids_service_amount(self, fsm_orders):
        account_ids_service_amount = float(0)
        orders = self.env['fsm.order'].sudo().search([['id','in',fsm_orders.ids],['partner_account','in',self.partner_account.ids]])
        for order in orders:
            account_ids_service_amount += float(order.service_amount)
        return account_ids_service_amount
    
    def get_channel_ids_service_amount(self, fsm_orders):
        channel_ids_service_amount = float(0)
        orders = self.env['fsm.order'].sudo().search([['id','in',fsm_orders.ids],['partner_channel','in',self.partner_channel.ids]])
        for order in orders:
            channel_ids_service_amount += float(order.service_amount)
        return channel_ids_service_amount

    def get_service_ids_service_amount(self, fsm_orders):
        service_ids_service_amount = float(0)
        orders = self.env['fsm.order'].sudo().search([['id','in',fsm_orders.ids],['service_id','in',self.service_id.ids]])
        for order in orders:
            service_ids_service_amount += float(order.service_amount)
        return service_ids_service_amount
    
    def get_subservice_ids_service_amount(self, fsm_orders):
        subservice_ids_service_amount = float(0)
        orders = self.env['fsm.order'].sudo().search([['id','in',fsm_orders.ids],['subservice_id','in',self.subservice_id.ids]])
        for order in orders:
            subservice_ids_service_amount += float(order.service_amount)
        return subservice_ids_service_amount