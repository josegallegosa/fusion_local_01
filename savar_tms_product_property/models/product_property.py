import base64
import requests

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class ProductProperty(models.Model):
    _name = "product.property"
    _inherit = ['image.mixin']
    _description = "Propiedades de los productos"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string='Nombre de la propiedad', index=True, required=True)
    complete_name = fields.Char(
        string='Complete Name', compute='_compute_complete_name', store=True)
    parent_id = fields.Many2one(
        string='Propiedad Padre', comodel_name='product.property',  index=True, ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_id = fields.One2many(
        string='Sub Propiedades', comodel_name='product.property', inverse_name='parent_id')

    odoo_image_url = fields.Char(
        string='URL a la imagen', compute='_compute_odoo_image_url')

    def _compute_odoo_image_url(self):
        web_base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        for record in self:
            record.odoo_image_url = f'{web_base_url}/web/image/{self._name}/{record.id}/image_256'

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for proper in self:
            if proper.parent_id:
                proper.complete_name = '%s / %s' % (
                    proper.parent_id.complete_name, proper.name)
            else:
                proper.complete_name = proper.name

    @api.constrains('parent_id')
    def _check_property_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive properties.'))
        return True

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]
