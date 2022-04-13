from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.template'

    #property_ids = fields.Many2many('product.template',string='Propiedades del producto')
    property_line_ids = fields.Many2many(
        'product.property', string='Propiedades del producto')
    product_property_list = fields.One2many('product.property',
                                            string='Lista de propiedades', compute='_compute_property_list')

    @api.depends('property_line_ids')
    def _compute_property_list(self):
        for record in self:
            # TODO replicar chekeo en todos los que son field dict
            if record.property_line_ids.ids:
                record.product_property_list = self.env['product.property'].search_read(
                    [('id', 'in', record.property_line_ids.ids)], ['name', 'odoo_image_url'])
            else:
                record.product_property_list = False
