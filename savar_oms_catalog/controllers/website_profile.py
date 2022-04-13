from odoo import http, _
from odoo.http import request
from odoo.exceptions import Warning, UserError
import werkzeug
import werkzeug.utils
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager

import logging, sys

_logger = logging.getLogger(__name__)

class CustomerPortalInerith(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name", "merchant_catalog_owner"]

    @http.route('/my/categories', auth='public', website=True)
    def my_categories(self, **kw):
        return http.request.render('savar_oms_catalog.portal_my_categories_webpage', kw)
    
    @http.route('/merchant/orders', auth='public', website=True)
    def merchant_orders(self, **kw):
        return http.request.render('savar_oms_catalog.portal_merchant_orders_webpage', kw)

    @http.route(['/merchant/order/new'], auth='public', website=True)
    def merchant_orders_new(self, **kw):
        return http.request.render('savar_oms_catalog.portal_merchant_orders_new_webpage',{})
    
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        return werkzeug.utils.redirect('/web')

    @http.route('/my/fsm_orders', auth='public', website=True)
    def merchant_orders(self, **kw):
        return http.request.render('savar_oms_catalog.portal_fsm_orders_webpage', kw)
    
    @http.route(['/merchant/order_service/new'], auth='public', website=True)
    def merchant_orders_new_fsm(self, **kw):
        return http.request.render('savar_oms_catalog.portal_merchant_fsm_orders_new_webpage',{})
    

    @http.route('/merchant/informe/fsm_order', auth='public', website=True)
    def merchant_informe_fsm_orders(self, **kw):

        user_id = request.env.user.id
        res = request.env['fsm.order'].sudo().get_bi_fsm_order()
        
        return request.render("savar_oms_catalog.portal_informe_fsm_orders_webpage", {'tabledata2':res[0]})

    @http.route('/merchant/informe/sale_order', auth='public', website=True)
    def merchant_informe_sale_orders(self, **kw):

        user_id = request.env.user.id
        res = request.env['sale.order'].sudo().get_bi_sale_order()
        
        return request.render("savar_oms_catalog.portal_informe_sale_orders_webpage", {'tabledata2':res[0]})


    def _prepare_portal_layout_values(self):
        """Values for /my/* templates rendering.
        Does not include the record counts.
        """
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        return {
            'sales_user': sales_user,
            'page_name': 'home',
        }
    
    @http.route(['/my/merchant_orders', '/my/merchant_orders/page/<int:page>'], type='http', auth="user", website=True)
    def merchant_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SaleOrder = request.env['sale.order']

        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', 'in', ['draft']),
            ('merchant_account', '=', partner.id),
        ]

        searchbar_sortings = {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        quotation_count = SaleOrder.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/merchant_orders",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=quotation_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        quotations = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_quotations_history'] = quotations.ids[:100]

        values.update({
            'date': date_begin,
            'quotations': quotations.sudo(),
            'page_name': 'Pedidos Mercantiles - Cotización',
            'pager': pager,
            'default_url': '/my/merchant_orders',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("sale.portal_my_quotations", values)

    @http.route(['/my/fsm_orders', '/my/fsm_orders/page/<int:page>'], type='http', auth="user", website=True)
    def fsm_orders(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        _fsm_order = request.env['fsm.order']
        quotations = request.env['fsm.order'].sudo().search([])

        _logger.warning('fsm_orders values')
        _logger.warning(values)
        
        return request.render("savar_oms_catalog.portal_fsm_orders_webpage", {'quotations':quotations})