from odoo import api, fields, models


class OmsPricelist(models.Model):
    _name = 'oms.pricelist'
    _description = 'New Description'

    name = fields.Char(string='Nombre', required=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', required=True)
    service_id = fields.Many2one('fsm.order.service', string='Servicio', required=True)
    service_name = fields.Char(string='Servicio', related='service_id.name')
    merchant_account = fields.Many2one('res.partner', string="Comerciante", domain="[('merchant_catalog_owner', '=', True)]")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    package_lump_amount = fields.Float(string='Monto Máximo del Bulto', required=True)

    pricelist_item1_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='General')
    pricelist_item2_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='Last Mile')
    pricelist_item3_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='FulFillment')
    pricelist_item4_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='Consolidado')