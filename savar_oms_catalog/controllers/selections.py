# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class selections(http.Controller):   

    @http.route(['/selections/product/get_uoms'], type='json', auth='public', methods=['POST'], website=True)
    def get_uoms(self, fields, domain):
        product_id = request.env['product.template'].browse(int(domain[0][2]))
        _logger.warning('get_uoms product_id')
        _logger.warning(product_id)
        domain = []
        _filter = ['category_id','=', int(product_id.uom_id.category_id)]
        domain.append(_filter)

        _logger.warning('get_uoms domain')
        _logger.warning(domain)

        can_create = request.env['uom.uom'].check_access_rights('create', raise_exception=False)       
        return {
                    'read_results': request.env['uom.uom'].search_read(domain, fields),
                    'can_create': can_create,
                } 
    
    @http.route(['/selections/partner/get_partners'], type='json', auth='public', methods=['POST'], website=True)
    def get_partners(self, fields, domain):
        can_create = request.env['res.partner'].check_access_rights('create', raise_exception=False)
        return {
                    'read_results': request.env['res.partner'].search_read(domain, fields),
                    'can_create': can_create,
                }
    
    @http.route(['/selections/partner/get_invoice_partner_childs'], type='json', auth='public', methods=['POST'], website=True)
    def get_invoice_partner_childs(self, fields, domain):
        can_create = request.env['res.partner'].check_access_rights('create', raise_exception=False)       
        return {
                    'read_results': request.env['res.partner'].search_read(domain, fields),
                    'can_create': can_create,
                }
        
    @http.route(['/selections/products/get_products'], type='json', auth='public', methods=['POST'], website=True)
    def get_products(self, fields, domain):
        can_create = request.env['product.template'].check_access_rights('create', raise_exception=False)
        return {
                    'read_results': request.env['product.template'].search_read(domain, fields),
                    'can_create': can_create,
                }    
    
    @http.route(['/selections/products/get_product_services'], type='json', auth='public', methods=['POST'], website=True)
    def get_products_services(self, product_id, fields):        
        product_id = request.env['product.template'].browse(int(product_id))
        
        _logger.warning("get_products_services product_id")
        _logger.warning(product_id)

        services_ids = []
        if(product_id):
            _logger.warning("get_products_services product_id.product_service_subservices")
            _logger.warning(product_id.read())
            _logger.warning(product_id.sudo().product_service_subservices)

            if(product_id.product_service_subservices):
                for service in product_id.product_service_subservices:
                    services_ids.append(service.id)

        domain = [['id','in',services_ids]]

        _logger.warning("get_products_services domain")
        _logger.warning(domain)

        can_create = request.env['fsm.order.service'].check_access_rights('create', raise_exception=False)
        read_results = request.env['fsm.order.service'].search_read(domain, fields)

        _logger.warning("get_products_services read_results")
        _logger.warning(read_results)

        if(read_results):
            index = 0
            for result in read_results:
                current_name = str(read_results[index]['name'])

                service = request.env['fsm.order.service'].browse(int(result['id']))
                parent_name = str("")
                if(service):
                    parent_name = str(service.parent_id.name) + str(' - ')                
                
                read_results[index]['name'] = str(parent_name) + str(current_name) 
                index += int(1)
                
                _logger.warning(result)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/service/get_services'], type='json', auth='public', methods=['POST'], website=True)
    def get_services(self, fields, domain):
        can_create = request.env['fsm.order.service'].check_access_rights('create', raise_exception=False)
        read_results = request.env['fsm.order.service'].search_read(domain, fields)
        if(read_results):
            index = 0
            for result in read_results:
                current_name = str(read_results[index]['name'])

                service = request.env['fsm.order.service'].browse(int(result['id']))
                parent_name = str("")
                if(service):
                    if(service.parent_id):
                        parent_name = str(service.parent_id.name) + str(' - ')                
                
                read_results[index]['name'] = str(parent_name) + str(current_name) 
                index += int(1)

        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/taxes/search_read'], type='json', auth='public', methods=['POST'], website=True)
    def slide_channel_tag_search_read(self, fields, domain):
        can_create = request.env['account.tax'].check_access_rights('create', raise_exception=False)
        return {
                    'read_results': request.env['account.tax'].search_read(domain, fields),
                    'can_create': can_create,
                }
    
    @http.route(['/selections/taxes/get_taxes_assigned'], type='json', auth='public', methods=['POST'], website=True)
    def get_taxes_assigned(self, fields, domain):
        taxes = request.env['product.template'].sudo().get_taxes_assigned(fields, domain)
        return taxes

    @http.route(['/selections/orders/fsm_payment_types'], type='json', auth='public', methods=['POST'], website=True)
    def get_payment_types(self, fields, domain):
        can_create = request.env['payment.type'].check_access_rights('create', raise_exception=False)
        read_results = request.env['payment.type'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/orders/fsm_by_packages'], type='json', auth='public', methods=['POST'], website=True)
    def get_shipping_type_ids(self, fields, domain):
        can_create = request.env['by.package'].check_access_rights('create', raise_exception=False)
        read_results = request.env['by.package'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/stock/get_locations'], type='json', auth='public', methods=['POST'], website=True)
    def get_locations(self, fields, domain):
        can_create = request.env['stock.location'].check_access_rights('create', raise_exception=False)
        read_results = request.env['stock.location'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/orders/get_fsm_account'], type='json', auth='public', methods=['POST'], website=True)
    def get_fsm_account(self, fields, domain):
        can_create = request.env['res.partner'].check_access_rights('create', raise_exception=False)
        read_results = request.env['res.partner'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/orders/get_fsm_account'], type='json', auth='public', methods=['POST'], website=True)
    def get_fsm_account(self, fields, domain):
        can_create = request.env['res.partner'].check_access_rights('create', raise_exception=False)
        read_results = request.env['res.partner'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }