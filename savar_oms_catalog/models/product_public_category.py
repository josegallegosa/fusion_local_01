# -*- coding: utf-8 -*-
from odoo import fields,models

class product_public_category(models.Model):
    _inherit = "product.public.category"

    merchant_account = fields.Many2one(string="Comerciante")

    def get_ecommerce_categories(self):
        ecommerce_categories = self.env["product.public.category"].sudo().search([
                                                                                    ( 'merchant_account', '=', int(merchant_id) )
                                                                                 ])
        return ecommerce_categories

    def get_partner_merchant(self, params):
        try:
            query = "select id, merchant_catalog_owner from res_partner where id = " + str(params['id'])
            _logger.warning('set_partner_merchant')
            _logger.warning(query)
            request.cr.execute(query)
            res_partner = request.cr.dictfetchone()
            return res_partner
        except:
            return 'not found'
            pass