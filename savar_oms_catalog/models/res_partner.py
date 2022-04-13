
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class res_partner(models.Model):
    _inherit = 'res.partner'

    merchant_catalog_owner = fields.Boolean(string="Comerciante")
    def get_partner_merchant(self, params):
        try:
            query = "select merchant_catalog_owner from res_partner where id = " + str(params['id'])
            request.cr.execute(query)
            res_partner = request.cr.dictfetchone()
            return res_partner
        except:
            return 'not found'
            pass

    def set_partner_merchant(self, params):
        try:     
            if( str(params['is_merchant']) == "False" ):
                query = "update res_partner set merchant_catalog_owner = True where id = " + str(self.env.user.id)
                _logger.warning('set_partner_merchant')
                _logger.warning(query)
                request.cr.execute(query)
                self.add_partner_user_to_merchant_group(for_assign=True)
            else:
                query = "update res_partner set merchant_catalog_owner = False where id = " + str(self.env.user.id)
                _logger.warning('set_partner_merchant')
                _logger.warning(query)
                request.cr.execute(query)
                self.add_partner_user_to_merchant_group(for_assign=False)            
        except:
            pass
    
    def add_partner_user_to_merchant_group(self, for_assign=True):
        merchant_account = self.env['res.groups'].sudo().search([['name','=','Cuenta Mercantil']], limit=1)
        _logger.warning("add_partner_user_to_merchant_group merchant_account")
        _logger.warning(merchant_account)
        if(merchant_account):
            if(for_assign):
                _logger.warning("add_partner_user_to_merchant_group for_assign=True ")
                merchant_account.users = [(4, self.env.user.id)]
            else:
                _logger.warning("add_partner_user_to_merchant_group for_assign=False ")
                merchant_account.users = [(3, self.env.user.id)]
    
    def get_partners(self, fields, domain):
        query = "select id as id, name as text from res_partner"
        request.cr.execute(query)    
        partners = request.cr.dictfetchall()
        return { 'partners':partners }