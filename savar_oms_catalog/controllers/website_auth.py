from odoo import http, _
from odoo.http import request
from odoo.exceptions import Warning, UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import logging, sys
_logger = logging.getLogger(__name__)

class AuthSignupHomeInerith(AuthSignupHome):
    def do_signup(self, qcontext):
        try:
            values1 = { key: qcontext.get(key) for key in ('login', 'name', 'password', 'merchant_catalog_owner') }
            
            _logger.warning('AuthSignupHomeInerith')
            _logger.warning(values1)

            values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
            if not values:
                raise UserError(_("The form was not properly filled in."))
            if values.get('password') != qcontext.get('confirm_password'):
                raise UserError(_("Passwords do not match; please retype them."))
            supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
            lang = request.context.get('lang', '').split('_')[0]
            if lang in supported_lang_codes:
                values['lang'] = lang
            self._signup_with_values(qcontext.get('token'), values)
            request.env.cr.commit()
            if(str(values1['merchant_catalog_owner'])=="on"):
                query = "update res_partner set merchant_catalog_owner= True where id = "+str(request.env.user.partner_id.id)
                _logger.warning('AuthSignupHomeInerith PSQL')
                _logger.warning(query)
                request.cr.execute(query)
                self.assign_user_to_merchant_group()
        except Exception as e:
            _logger.warning(getattr(e, 'message', repr(e))+" ON LINE "+format(sys.exc_info()[-1].tb_lineno))

    def assign_user_to_merchant_group(self):
        request.env['res.partner'].sudo().add_partner_user_to_merchant_group()