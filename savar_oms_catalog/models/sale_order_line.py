from odoo import models, fields, api
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    product_service_subservices = fields.Many2many(string='SubServicios',related='product_id.product_service_subservices') 
    subservice_id = fields.Many2one('fsm.order.service', string='SubServicio')

    @api.onchange('product_id')
    def _onchange_oms_product_id(self):
        self.subservice_id = None