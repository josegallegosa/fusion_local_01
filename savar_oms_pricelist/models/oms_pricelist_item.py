from odoo import api, fields, models

class OmsPricelistItem(models.Model):

    _name = 'oms.pricelist.item'
    _description = 'New Description' 
    
    pricelist_id = fields.Many2one('oms.pricelist', string='Pricelist')
    service_name = fields.Char(string='Servicio', related='pricelist_id.service_id.name')
    
    subservice_id = fields.Many2one('fsm.order.service', string='SubServicio')
    warehouse_id = fields.Many2one('stock.warehouse', string='Local')
    district_id = fields.Many2one('res.district', string='Zona')
    sufix = fields.Char(string='Sufijo')
    size_id = fields.Many2one('product.size', string='Talla')
    size_quant = fields.Integer(string='Cantidad Talla')
    failed_recount = fields.Integer(string='Fallidas', default=0)
    failed_amount_charge = fields.Float(string='Cargo')
    price = fields.Float(string='Tarifa')


    ubigeo_id= fields.Many2one('ubigeo', string='Ubigeo')
    storage_id= fields.Many2one('storage', string='Almacenaje')
    labeling_products_id= fields.Many2one('labeling.product', string='Etiq. Producto')
    labeling_packages_id= fields.Many2one('labeling.package', string='Etiq. Paquete')
    by_weight_id= fields.Many2one('by.weight', string='Por Peso')
    by_package_id= fields.Many2one('by.package', string='Por Bultos')
    payment_type_id= fields.Many2one('payment.type', string='Tipo De Pago')
    picking_id= fields.Many2one('picking', string='picking')
    packing_id= fields.Many2one('packing', string='packing')
    by_pick_up_id= fields.Many2one('by.pick.up', string='Por Recojo')
    by_sure_id= fields.Many2one('by.sure', string='Por Seguro')
    back_office_id= fields.Many2one('back.office', string='Back Office')
    prints_id= fields.Many2one('prints', string='Impresiones')    