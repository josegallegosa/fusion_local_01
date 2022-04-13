# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
import logging
_logger = logging.getLogger(__name__)

class fsm_order(models.Model):
    _inherit = 'fsm.order'

    def update_stage(self, params):
        stage_id = params['stage_id']
        stage = request.env['fsm.stage'].sudo().search([['id','=',int(stage_id)]])        
        return stage

    @api.model
    def _get_move_domain(self):
        return [("picking_id.picking_type_id.code", "in", ("outgoing", "incoming"))]

    sale_order = fields.Many2one(comodel_name='sale.order',inverse_name="fsm_order_ids", string="Pedido")
    package_lump_ids = fields.Many2many("package.lump", inverse_name="fsm_order_id", string="Montos Referenciados")

    @api.onchange('package_lump_ids')
    def _package_lump_amount(self):
        total = float(0.0)
        for record in self:
            for lump in self.package_lump_ids:
                if( lump.amount ):
                    if( float(lump.amount)  > 0 ):
                        total += float(lump.amount)
        self.package_lump_amount = total

    package_lump_amount = fields.Float(string="Monto Total (bultos)", readonly=False, store=True)

    def get_fsm_location(self, location):
        domain = []
        _fsm_location = None
        if('state_id' in location):
            domain.append(['state_id', '=', int(location['state_id'])])
        if('province_id' in location):
            domain.append(['province_id', '=', int(location['province_id'])])
        if('district_id' in location):
            domain.append(['distrito_id', '=', int(location['district_id'])])
        
        _logger.warning('get_fsm_location domain')
        _logger.warning(domain)

        _fsm_location = request.env['fsm.location'].sudo().search(domain)

        _logger.warning('get_fsm_location location')
        _logger.warning(_fsm_location)
        _logger.warning(_fsm_location.complete_name)

        return _fsm_location
    
    def get_merchant_fsm_order(self, params):
        return request.env['fsm.order'].sudo().search([['code_merchant', '=', str(params['code_merchant'])]])

    def create_merchant_fsm_order(self, _params):
        _logger.warning("----------- FSM ORDER --------------")

        # verify if order already exist with merchant code only
        params = {'code_merchant': str(_params['code_merchant'])}
        _fsm_order = self.get_merchant_fsm_order(params)
        if(_fsm_order):
            return {'error':True, 'code':'DUPLICATED'}

        order = {
                    'name': str(_params['name']),
                    'code_merchant': str(_params['code_merchant']),
                    'service_id': int(_params['service_id']),
                    'subservice_id': int(_params['subservice_id']),
                    'shipping_type_id': str(_params['shipping_type_id']),
                    'by_package_id': int(_params['by_package_id']),
                    'payment_type_id': int(_params['payment_type_id']),
                    'consigned_id': str(_params['consigned_id']),
                    'appointment_time_from': str(_params['fsm_start_time']),
                    'appointment_time_until': str(_params['fsm_ends_time']),
                }

        # sub_stage_id
        if('sub_stage_id' in _params):
            order['sub_stage_id'] = _params['sub_stage_id']
            
        # priority
        if('priority' in _params):
            order['priority'] = _params['priority']

        # description
        if('description' in _params):
            order['description'] = _params['description']

        # instructions
        if('todo' in _params):
            order['todo'] = _params['todo']

        if('date_dispatch' in _params):
            order['date_dispatch'] = _params['date_dispatch']

        if('location' in _params):
            location_id = self.get_fsm_location(_params['location'])
            if(location_id):
                order['location_id'] = int(location_id.id)

        _logger.warning("----------- BG CREATE FSM ORDER --------------")
        _logger.warning("create_merchant_fsm_order order")
        _logger.warning(order)

        fsm_order = request.env['fsm.order'].sudo().create(order)

        _logger.warning("fsm order")
        _logger.warning(fsm_order.read())
        _logger.warning("************************")
        _logger.warning(_params)
        _logger.warning("************************")
        _logger.warning("----------- EOF CREATE FSM ORDER ------------")

        if(fsm_order):
            if('stock_quants' in _params):
                self.create_fms_order_inventory(_params['stock_quants'], fsm_order)
                
                pass
            return fsm_order
        return None
    
    def sync_package_lumps_importer(self, fsm_order):
        collection = []
        if(fsm_order.move_ids):
            _logger.warning("fsm_order.move_ids")
            _logger.warning(fsm_order.move_ids)
            for move in fsm_order.move_ids:
                move.sudo().update({'fsm_order_id':int(fsm_order.id)})
                move.picking_id.sudo().update({'fsm_order':int(fsm_order.id)})
                _logger.warning("$$$ stock_picking")
                _logger.warning(move.picking_id)
                _logger.warning(move.fsm_order_id)
                _logger.warning("move.package_lump")
                _logger.warning(move.package_lump)
                if(move.package_lump):
                    try:
                        _key = collection[str(move.package_lump).upper()]
                        _logger.warning("_key")
                        _logger.warning(_key)
                        _logger.warning(" --* WITH package_lump *--")                        
                    except:
                        _logger.warning(" --* WITHOUT package_lump *--")
                        collection.append(move.package_lump)
                        pass

        _logger.warning("collection")
        _logger.warning(collection)

        ids = []
        if( len(collection) > 0 ):            
            for _key in collection:
                package_lump = None
                domain = [
                            ['name','=',str(_key)],
                            ['fsm_order_id','=',int(self._origin.id)]
                         ]
                _logger.warning("domain")
                _logger.warning(domain)
                has_package_lump = request.env['package.lump'].sudo().search(domain, limit=1)
                _logger.warning("has_package_lump")
                _logger.warning(has_package_lump)
                if( not has_package_lump ):
                    package_lump_vals = {
                                            'name': str(_key),
                                            'amount': float(0.00),
                                            'fsm_order_id': int(self._origin.id)
                                        }
                    package_lump = request.env['package.lump'].sudo().create(package_lump_vals)
                    _logger.warning("package_lump")
                    _logger.warning(package_lump)
                if(package_lump):
                    ids.append(package_lump.id)
                else:
                    _logger.warning('has_package_lump')
                    _logger.warning(has_package_lump.id)
                    ids.append(has_package_lump.id)
                    pass
            if(len(ids)):
                fsm_order.sudo().update({
                                        'package_lump_ids':[[6,0,ids]]
                                    })
            _logger.warning("ids")
            _logger.warning(ids)

        return ids
    
    def create_fms_order_inventory(self, stock_quants, fsm_order):
        _logger.warning('create_fms_order_inventory stock_quants')
        _logger.warning(stock_quants)
        
        input_type = 'outcoming'
        
        if( str(fsm_order.service_id.name) == str('Last Mile') ):
            _logger.warning('fsm_order.service_id.name')
            _logger.warning(str(fsm_order.service_id.name))
            if(stock_quants):
                for stock_quant in stock_quants:
                    _logger.warning('fsm_order.service_id.name')
                    _logger.warning(stock_quant)
                    package_lump_vals = {
                                            'name': str(stock_quant['package_lump']),
                                            'amount': float(0.00),
                                            'fsm_order_id': int(fsm_order.id)
                                        }
                    package_lump = request.env['package.lump'].sudo().create(package_lump_vals)
                    
                    ids = []
                    if(fsm_order.package_lump_ids):
                        for lump_ids in fsm_order.package_lump_ids:
                            ids.append(int(lump_ids.id))
                    if(package_lump):
                        ids.append(int(package_lump.id))
                        _logger.warning('package_lump_ids')
                        _logger.warning([[0,6,ids]])
                        fsm_order.sudo().update( { 'package_lump_ids': None } )
                        _lumps = request.env['package.lump'].sudo().search([['id','in',ids]])
                        fsm_order.sudo().update( { 'package_lump_ids': _lumps } )

        else:
            if(stock_quants):
                for stock_quant in stock_quants:
                    _logger.warning(stock_quant)
                    _product = request.env['product.product'].sudo().search([
                                                                                ['product_tmpl_id','=',int(stock_quant['product_id'])]
                                                                            ])
                    _logger.warning('_product')
                    _logger.warning(_product)
                    if(_product):
                        stock_quant['product_id'] = int(_product.id)

                        # BGN STOCK.QUANTS for a fsm picking
                        # -------------------------------------------------------------------------------------------------------------
                        create_stock_quants = False
                        if(create_stock_quants):                    
                            _stock_quant = request.env['stock.quant'].sudo().search([
                                                                                        ['product_id','=', int(stock_quant['product_id'])],
                                                                                        ['location_id','=', int(stock_quant['location_id'])],
                                                                                    ])
                            if(not _stock_quant):  
                                _logger.warning('creating...')
                                _stock_quant = request.env['stock.quant'].sudo().create(stock_quant)
                                _stock_quant.sudo().update({
                                                            'quantity': int(stock_quant['quantity']),
                                                            })
                            else:
                                _logger.warning('updating...')
                                _stock_quant.sudo().update({
                                                            'quantity': int(stock_quant['quantity']),
                                                            })
                            if(_stock_quant):
                                _logger.warning(_stock_quant.read())
                        
                        # EOF STOCK.QUANTS for a fsm picking
                        # -------------------------------------------------------------------------------------------------------------

                        # BGN STOCK.PICKING for a fsm picking
                        # -------------------------------------------------------------------------------------------------------------
                        stock_picking_type_fsm = request.env['stock.picking.type'].sudo().search([
                                                                                            ['sequence_code', '=', str('fsm.orders.transfers')]
                                                                                        ]
                                                                                        ,limit=1)
                        _logger.warning('stock_picking_type_fsm')
                        _logger.warning(stock_picking_type_fsm)
                        
                        stock_picking = None
                        
                        if(input_type == 'outcoming'):
                            _stock_location_dst = request.env['stock.location'].sudo().search([['fsm_input_type','=','dispatch']], limit=1)
                            stock_picking_values = {
                                                        'location_id':int(stock_quant['location_id']), 
                                                        'picking_type_id':int(stock_picking_type_fsm.id)
                                                    }
                                                
                            if(_stock_location_dst):
                                stock_picking_values['location_dest_id'] = int(_stock_location_dst.id)
                                stock_picking = request.env['stock.picking'].sudo().create(stock_picking_values)
                        

                        # BGN STOCK.MOVE for a fsm picking
                        # -------------------------------------------------------------------------------------------------------------                                         

                        if(input_type == 'outcoming'):
                            uom_id = int(_product.uom_id.id)
                            if('uom_id' in stock_quant):
                                if(stock_quant['uom_id']):
                                    uom_id = int(stock_quant['uom_id'])
                            
                            vals = {
                                        'name': str('Cantidad de producto actualizada'),
                                        'location_id': int(stock_quant['location_id']),
                                        'location_dest_id': int(stock_quant['location_id']),                                                                        
                                        'product_id': int(_product.id),
                                        'product_uom': int(uom_id),
                                        'product_uom_qty': int(stock_quant['quantity']),
                                        'picking_id':int(stock_picking.id),
                                        'fsm_order_id': int(fsm_order.id)
                                    }
                            _logger.warning("Warning vals")
                            _logger.warning(vals)
                            
                            move = request.env['stock.move'].sudo().create(vals)  
                            _logger.warning(move.read())
                            #raise Warning("IN")
                            fsm_order.sudo().update({
                                                        'move_ids': [(4, int(move.id))]
                                                    })
                                        
                        if(input_type == 'incoming'):
                            move = request.env['stock.move'].sudo().search([
                                                                                ['name','=', str('Cantidad de producto actualizada')],
                                                                                ['location_id','=', int(stock_quant['location_id'])],
                                                                                ['location_dest_id','=', int(stock_quant['location_id'])],
                                                                                ['product_id','=', int(_product.id)],
                                                                                ['product_uom','=', int(_product.uom_id.id)],
                                                                                
                                                                            ],limit=1)
                            if(not move):
                                pass
                                move = request.env['stock.move'].sudo().create({
                                                                                    'name': str('Cantidad de producto actualizada'),
                                                                                    'location_id': int(stock_quant['location_id']),
                                                                                    'location_dest_id': int(stock_quant['location_id']),                                                                        
                                                                                    'product_id': int(_product.id),
                                                                                    'product_uom': int(stock_quant['uom_id']),
                                                                                    'product_uom_qty': int(stock_quant['quantity']),
                                                                                    'picking_id':int(stock_picking.id),
                                                                                    'fsm_order_id': int(fsm_order.id)
                                                                                }) 
                                fsm_order.sudo().update({
                                                            'move_ids': [(4, int(move.id))]
                                                        })                       
                            else:
                                move.sudo().update({
                                                        #'name': str('Cantidad de producto actualizada'),
                                                        'location_id': int(stock_quant['location_id']),
                                                        'location_dest_id': int(stock_quant['location_id']),                                                                        
                                                        'product_id': int(_product.id),
                                                        'product_uom': int(stock_quant['uom_id']),
                                                        'product_uom_qty': int(stock_quant['quantity']),
                                                        'picking_id':int(stock_picking.id),
                                                        'fsm_order_id': int(fsm_order.id)
                                                    })
                                fsm_order.sudo().update({
                                                            'move_ids': [(4, int(move.id))]
                                                        })  
                        
                        if(stock_picking):
                            _logger.warning('stock_picking')                                           
                            _logger.warning(stock_picking.name) 
                            _logger.warning('stock_picking move picking') 
                            _logger.warning(move.picking_id.name) 
                        
                        # extra fields
                        if(move):
                            if('package_lump' in stock_quant):
                                if(len(stock_quant['package_lump'])>0):
                                    move.sudo().update({
                                                            'package_lump': str(stock_quant['package_lump'])
                                                        })                    
                        if(move):
                            try:
                                _logger.warning(move)
                                move._action_confirm()
                                move._action_assign()
                                move.move_line_ids.write({                                                    
                                                            'qty_done': int(stock_quant['quantity'])
                                                        })
                                move._action_done()
                            except:
                                pass

                        # EOF STOCK.MOVE for a fsm picking
                        # -------------------------------------------------------------------------------------------------------------

                            fsm_order_inventories = []
                            
                            try:
                                if(fsm_order.move_ids):
                                    for _move in fsm_order.move_ids:
                                        fsm_order_inventories.append(int(_move.id))
                                        _move.sudo().update({'fsm_order_id': int(fsm_order.id)})
                                        _logger.warning("BGN fsm_order_id ================================")
                                        _logger.warning(fsm_order_inventories)
                                        _logger.warning(_move.fsm_order_id)
                                        _logger.warning("EOF fsm_order_id ================================")
                                fsm_order_inventories.append(int(move.id))                            
                                
                            except:
                                pass
                            
                            self.sync_package_lumps_importer(fsm_order)
                        

    def get_appointments_range_time(self):
        return self._fields['appointment_time_from'].selection
    

    @api.model
    def get_bi_fsm_order(self):
        res = []
       
        query4="""
                SELECT 
				SERVICE.NAME SERVICE
				,SUBSERVICE.NAME SUBSERVICE
				,SHIPPING.NAME SHIPPING_TYPE
                ,PACKAGE.NAME BY_PACKAGE
                ,PAYMENT.NAME PAYMENT_TYPE
                ,SUM(SERVICE_AMOUNT) SERVICE_AMOUNT --MONTO DEL SERVICIO
                ,COUNT(*) COUNT --MONTO DEL SERVICIO
                FROM FSM_ORDER ORDER_
				LEFT JOIN FSM_ORDER_SERVICE SERVICE ON ORDER_.SERVICE_ID = SERVICE.ID
				LEFT JOIN FSM_ORDER_SERVICE SUBSERVICE ON ORDER_.SUBSERVICE_ID = SUBSERVICE.ID
				LEFT JOIN SHIPPING_TYPE SHIPPING ON ORDER_.SHIPPING_TYPE_ID = SHIPPING.ID
				LEFT JOIN BY_PACKAGE PACKAGE ON ORDER_.BY_PACKAGE_ID = PACKAGE.ID
				LEFT JOIN PAYMENT_TYPE PAYMENT ON ORDER_.PAYMENT_TYPE_ID = PAYMENT.ID
				
				GROUP BY SERVICE.NAME
				,SUBSERVICE.NAME
				,SHIPPING.NAME
                ,PACKAGE.NAME 
                ,PAYMENT.NAME 
        """
        self._cr.execute(query4)
        table2 = self._cr.dictfetchall()

        res.append(table2)

        return res