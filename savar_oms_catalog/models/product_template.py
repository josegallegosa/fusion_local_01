# -*- coding: utf-8 -*-
from odoo import fields,models
import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = "product.template"

    product_service_subservices = fields.Many2many('fsm.order.service', string='Servicio / Subservicio')
    
    def get_sale_taxes(self):
        return self.env['account.tax'].sudo().get_account_taxes_for_sale()
    
    def get_taxes_assigned(self, fields, domain):
        product_template = self.env['product.template'].sudo().search(domain)
        taxes = []
        taxes_preselection = []
        if(product_template):
            if(product_template.taxes_id):
                for taxes_ids in product_template.taxes_id:
                    taxes_preselection.append(int(taxes_ids.id))
                    tax = {
                            'id': str(taxes_ids.id) ,
                            'text': str(taxes_ids.name) ,
                          }
                    taxes.append(tax)
        return { 
                'taxes_preselection':taxes_preselection, 
                'taxes':taxes 
               }
    
    def save_values(self, params):
        product_template = self.env['product.template'].browse(int(params['id']))
        _logger.warning(product_template)
        if('name' in params):
            _logger.warning("save_values")
            _logger.warning(params['name'])
            product_template.sudo().update({'name':params['name']})
        if('list_price' in params):
            product_template.update({'list_price':params['list_price']})
        if('default_code' in params):
            product_template.update({'default_code':params['default_code']})
        if('barcode' in params):
            product_template.update({'barcode':params['barcode']})
        if('public_description' in params):
            product_template.update({'public_description':params['public_description']})
        if('product_stock' in params):
            product_template.update({'virtual_available':params['product_stock']})
        
        if('product_subservice' in params):
            services = []
            _services = []
            _logger.warning('product_subservice')
            _logger.warning(params['product_subservice'])         
            if(params['product_subservice']):
                services = str(params['product_subservice']).split(",")
                for service in services:
                    _services.append(int(service))
                _logger.warning(_services)
                self.env['product.template'].update({'product_service_subservices':[[6,0,_services]]})
        
        if('taxes_id' in params):
            taxes = []
            if(params['taxes_id']):
                for tax in params['taxes_id']:
                    taxes.append(tax)

            self.env['product.template'].update({'taxes_id':[6,0,taxes]})