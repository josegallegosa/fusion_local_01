# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class stock_move(models.Model):
    _inherit = 'stock.move'
    
    package_lump = fields.Char(string="Bulto")

    """
    def _compute_movement_type(self):
        try:
            if(self):
                for record in self:
                    if(record.picking_id.picking_type_code):
                        if(record.picking_id.picking_type_code == "outgoing" or record.picking_id.picking_type_code == "incoming"):
                            code = str()
                            if(record.picking_id.picking_type_code == "outgoing"):
                                code = 'Despacho'
                            if(record.picking_id.picking_type_code == "incoming"):
                                code = 'Ingreso'
                            record.movement_type = code
                        else:
                            record.movement_type = None
        except:
            record.movement_type = None
            pass
    """
    