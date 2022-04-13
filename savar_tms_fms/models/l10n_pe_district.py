from odoo import models, fields, api


class L10nPeDistrict(models.Model):
    _inherit = 'l10n_pe.res.city.district'

    zone_type_id = fields.Many2one('res.zone.type', string='Tipo de zona')
    state_id = fields.Many2one('res.country.state', related='city_id.state_id')
    country_id = fields.Many2one('res.country', related='city_id.country_id')