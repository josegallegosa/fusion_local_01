from odoo import api, fields, models


class FsmLocation(models.Model):
    _inherit = 'fsm.location'

    province_id = fields.Many2one('res.country.state', 'Provincia')
    distrito_id = fields.Many2one('res.country.state', 'Distrito')
    partner_id = fields.Many2one(
        "res.partner",
        string="Related Partner",
        required=False,
        ondelete="restrict",
        delegate=True,
        auto_join=True,
    )
    owner_id = fields.Many2one(
        "res.partner",
        string="Related Owner",
        required=False,
        ondelete="restrict",
        auto_join=True,
    )
    contact_id = fields.Many2one(
        "res.partner",
        string="Primary Contact",
        domain="[('is_company', '=', False)," " ('fsm_location', '=', False)]",
        index=True,
        required=False,
    )

    @api.onchange('street')
    @api.onchange('zip')
    def onchange_geo_localize(self):
        self.geo_localize()
    
    @api.onchange('distrito_id')
    def onchange_distrito_id(self):
        self.zip = self.distrito_id.code