# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class stock_picking(models.Model):
    _inherit = 'stock.picking'

    fsm_order = fields.Many2one("fsm.order", string="Pedido de Trabajo")

    def write(self, vals):
        response = super().write(vals)
        fsm_order = request.env['fsm.order'].sudo().browse(int(self.fsm_order.id))
        ids = []
        for operation in self.move_ids_without_package:
            _logger.warning('operation')
            _logger.warning(operation)
            if(self.fsm_order):
                operation.sudo().update({
                                            'fsm_order_id': int(self.fsm_order.id)
                                        })
            if(fsm_order.move_ids):
                
                for move in fsm_order.move_ids:
                    if(int(operation.id) != int(move.id)):
                        ids.append(int(move.id))
                        
            ids.append(int(operation.id))
        _logger.warning('ids')
        _logger.warning(ids)
        if(len(ids)):
            _logger.warning('write')
            _logger.warning({'move_ids':[[0,6,ids]]})
            fsm_order.sudo().update({
                                        'move_ids':[[6,0,ids]],
                                    })
        return response