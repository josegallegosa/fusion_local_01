from odoo import api, fields, models

class res_partner(models.Model):
    _inherit = 'res.partner'

    is_ot_account = fields.Boolean(string="Es Cuenta OT")
    is_ot_channel = fields.Boolean(string="Es Canal OT")


    accounts_ids = fields.Many2many('res.partner','partner_accounts',column1="col_partner_1", column2="col_account",string='Cuentas Relacionadas',domain="[('is_ot_account', '=', True)]")
    channels_ids = fields.Many2many('res.partner','partner_accounts',column1="col_account", column2="col_partner_1",string='Canales Relacionados',domain="[('is_ot_channel', '=', True)]")
    
    
    @api.onchange('is_ot_account')
    def _onchange_is_ot_account(self):
        if self.is_ot_account == True:
            self.is_ot_channel = False
    
    @api.onchange('is_ot_channel')
    def _onchange_is_ot_channel(self):
        if self.is_ot_channel == True:
            self.is_ot_account = False
