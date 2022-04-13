# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class selections_location(http.Controller):
    @http.route(['/selections/orders/fsm_location_contries'], type='json', auth='public', methods=['POST'], website=True)
    def get_countries(self, fields, domain):
        can_create = request.env['res.country'].check_access_rights('create', raise_exception=False)
        read_results = request.env['res.country'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
    
    @http.route(['/selections/orders/fsm_location_states'], type='json', auth='public', methods=['POST'], website=True)
    def get_states(self, fields, domain):
        can_create = request.env['res.country.state'].check_access_rights('create', raise_exception=False)
        read_results = request.env['res.country.state'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }

    @http.route(['/selections/orders/fsm_location_provices'], type='json', auth='public', methods=['POST'], website=True)
    def get_provices(self, fields, domain):
        can_create = request.env['res.country.state'].check_access_rights('create', raise_exception=False)
        read_results = request.env['res.country.state'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }
                  
    @http.route(['/selections/orders/fsm_location_districts'], type='json', auth='public', methods=['POST'], website=True)
    def get_districts(self, fields, domain):
        can_create = request.env['res.country.state'].check_access_rights('create', raise_exception=False)
        read_results = request.env['res.country.state'].search_read(domain, fields)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }