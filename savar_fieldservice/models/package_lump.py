from odoo import api, fields, models


class package_lump(models.Model):
    _name = "package.lump"
    _description = "Paquete del bulto"

    name = fields.Char(string="Referencia")

    # refers to a count while distinc just collects one label for this package lump
    qty_distinc = fields.Char(string="Cantidad Distinguida")

    amount = fields.Float(string="Monto")
    total = fields.Char(string="Total")
    fsm_order_id = fields.Many2one("fsm.order", string="Pedido de Trabajo")