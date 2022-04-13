from odoo import models, fields, _
from odoo.http import request
import xlrd, xlwt
import base64
import logging
_logger = logging.getLogger(__name__)

class xlsx_templates(models.Model):
    _name = 'xlsx.templates'
    _description = 'Plantillas XLSX para Ordenes de Trabajo'

    name = fields.Char(string="XLSX")
    xlsx_file = fields.Binary(string="Archivo")
    service_id = fields.Many2one('fsm.order.service', string='Servicio')

    def get_templates(self, _args):
        xlsx_template = request.env['xlsx.templates'].search([])
        if(xlsx_template):
            return xlsx_template.read()
        else:
            return None
    
    def download_template(self, _args):
        xlsx_template = request.env['xlsx.templates'].search([['id','=',_args['id_xlsx']]])

        _logger.warning('xlsx_template')
        _logger.warning(xlsx_template.xlsx_file)

        if(xlsx_template):
            return {
                'name': str(xlsx_template.name),
                'type': 'ir.actions.act_url',
                'url': '/web/content/?model=xlsx.templates&id={}&field=xlsx_file&filename_field=name&download=true'.format(
                    int(_args['id_xlsx'])
                ),
                'target': 'self',
            }