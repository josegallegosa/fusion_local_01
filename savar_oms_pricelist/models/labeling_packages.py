from odoo import api, fields, models


class LabelingPackages(models.Model):
    _name = 'labeling.package'
    _description = 'Etiquetado Paquetes'

    name = fields.Char(string='Etiquetado Paquete')
    description = fields.Text(string='Descripción')

    