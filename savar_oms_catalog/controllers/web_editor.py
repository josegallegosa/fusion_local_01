from odoo.addons.web_editor.controllers.main import Web_Editor
from odoo.http import request
from odoo import http, tools, _, SUPERUSER_ID
import logging, sys
_logger = logging.getLogger(__name__)

class web_editor(Web_Editor):

    @http.route("/web_editor/public_render_template", type="json", auth="public", website=True)
    def public_render_template(self, args):
        response = super(web_editor, self).public_render_template(args)
        # args[0]: xml id of the template to render
        # args[1]: optional dict of rendering values, only trusted keys are supported
        
        _logger.warning('public_render_template args')
        _logger.warning(args)

        return response