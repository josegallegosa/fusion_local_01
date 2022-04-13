
from odoo import api, models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = 'sale.order'

    merchant_account = fields.Many2one('res.partner', string="Comerciante", domain="[('merchant_catalog_owner', '=', True)]")
    fsm_order_ids = fields.One2many(comodel_name='fsm.order', inverse_name="sale_order", string="Pedidos FSM")
    
    def get_fsm_orders_count(self):
        partner = request.env.user.partner_id
        domain = [ 
                    ['merchant_account', '=', int(partner.id)]
                 ]
        # domain
        orders = request.env['fsm.order'].sudo().search([])
        _logger.warning("orders get_merchant_orders_count")
        _logger.warning(orders)
        _logger.warning(domain)
        count = int(0)
        if(orders):
            count = len(orders)
        else:
            count = 0
        return count

    def get_merchant_orders_count(self):
        partner = request.env.user.partner_id
        domain = [ 
                    ['merchant_account', '=', int(partner.id)]
                 ]
        orders = request.env['sale.order'].sudo().search(domain)
        _logger.warning("orders get_merchant_orders_count")
        _logger.warning(orders)
        _logger.warning(domain)
        count = int(0)
        if(orders):
            count = len(orders)
        else:
            count = 0
        return count

    
    @api.model
    def get_bi_sale_order(self):
        res = []
       
        query4="""
                SELECT 
                CAST(DATE_ORDER AS DATE) DATE_ORDER
                ,STATE_.NAME DEPARTMENT
                ,PRODUCT.DEFAULT_CODE
                ,COUNT( DISTINCT PRODUCT_ID) CANT_PRODUCTOS
                ,SUM(0) AMOUNT_TAX
                ,SUM(ORDER_LINE.PRICE_SUBTOTAL) PRICE_SUBTOTAL
                ,SUM(ORDER_LINE.PRICE_SUBTOTAL+0) PRICE_TOTAL
                
                FROM SALE_ORDER 
                LEFT JOIN SALE_ORDER_LINE ORDER_LINE  ON ORDER_LINE.ORDER_ID = SALE_ORDER.ID
                LEFT JOIN PRODUCT_PRODUCT PRODUCT ON ORDER_LINE.PRODUCT_ID = PRODUCT.ID 
                LEFT JOIN FSM_LOCATION ON SALE_ORDER.FSM_LOCATION_ID = FSM_LOCATION.ID
                LEFT JOIN RES_COUNTRY_STATE STATE_ ON FSM_LOCATION.STORE_STATE_ID = STATE_.ID  
                --WHERE SALE_ORDER.NAME = 'S00007'
                GROUP BY 
                CAST(DATE_ORDER AS DATE)
                ,STATE_.NAME
                ,PRODUCT.DEFAULT_CODE
        """
        self._cr.execute(query4)
        table2 = self._cr.dictfetchall()

        res.append(table2)

        return res