from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning
from odoo.http import request
import logging, sys
_logger = logging.getLogger(__name__)


class FsmOrder(models.Model):
    _inherit = 'fsm.order'
    
    sub_stage_id = fields.Many2one(
        "fsm.stage.status",
        string="Sub-Status",
        required=True,
        tracking=True,
        #default=lambda self: self._default_stage_id().sub_stage_id,
    )

    location_id = fields.Many2one(
        "fsm.location", string="Location", index=True, required=False, domain="[('distrito_id', '!=', False)]"
    )

    partner_account = fields.Many2one("res.partner", string="Cuenta",domain="[('is_ot_account', '=', True)]")
    partner_channel = fields.Many2one("res.partner", string="Canal",domain="[('is_ot_channel', '=', True)]")

    package_lump_ids = fields.Many2many("package.lump", inverse_name="fsm_order_id", string="Montos Referenciados")    

    consigned_id = fields.Many2one("res.partner", string="Nombre del consignado", related='location_id.contact_id')
    consigned_dni = fields.Char(string="DNI Consignado", related='consigned_id.vat')
    consigned_district = fields.Many2one("fsm.location",string="Distrito Consignado",related='location_id.fsm_parent_id')
    consigned_reference = fields.Char(string="Referencia Consignado",related='location_id.street2')
    consigned_movil = fields.Char(string="Movil Consignado",related='location_id.phone')
    consigned_mail = fields.Char(string="Correo Consignado",related='location_id.email')

    def action_complete(self):
        raise UserError(str(self.stage_id.name))
    
    def action_cancel(self):
        raise UserError(str(self.stage_id.name))
    
    def fsm_action_complete(self):
        pass
    
    def fsm_action_cancel(self):
        pass
    
    def notification_allowed(self, model_ids, field_ids):
        _domain = [ ( '_models_001', 'in', model_ids ),  
                    ('_fields_001','in',field_ids),                    
                  ]
        if(self.stage_id):
            _domain.append(('_stages_ids','in',[int(self.stage_id.id)]))
             
        notificators = self.env['notificator.configurator'].sudo().search( _domain )
        if(notificators):
            return True
        else:
            return False

    @api.onchange('partner_channel')
    def _onchange_partner_channel(self):
        if self.partner_channel:
            return {'domain': {'partner_account': [('is_ot_account', '=', True),('id', 'in', self.partner_channel.accounts_ids.ids)] }}
        else:
            return {'domain': {'partner_account': [('is_ot_account', '=', True)] }}
    
    @api.onchange('partner_account')
    def _onchange_partner_account(self):
        if self.partner_account:
            return {'domain': {'partner_channel': [('is_ot_channel', '=', True),('id', 'in', self.partner_account.channels_ids.ids)] }}
        else:
            return {'domain': {'partner_channel': [('is_ot_channel', '=', True)] }}

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
    history_fields = fields.Text(string="History")

    # @api.onchange('move_ids')
    def sync_package_lumps(self):
        collection = []
        if(self.move_ids):
            _logger.warning("self.move_ids")
            _logger.warning(self.move_ids)
            for move in self.move_ids:
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
                self.sudo().update({
                                        'package_lump_ids':[[6,0,ids]]
                                    })
            _logger.warning("ids")
            _logger.warning(ids)

        return ids
    
    def update(self, vals):
        response = super().update(vals)
        _logger.warning('validate_package_lumps')
        return response

    def write(self, vals):
        _logger.warning('validate_package_lumps')
        response = super().write(vals)
        try:
            self.sudo().sync_package_lumps()
        except:
            pass
        #self.sudo().validate_package_lumps()                   })
        return response

    def validate_package_lumps(self):
        _logger.warning('validate_package_lumps')
        _logger.warning(self.package_lump_ids)
        if(not self.package_lump_ids):
            raise Warning("Debe existir un bulto asignado. Defina en lineas de SKU una etiqueta de bulto para operar con bultos.")

    def action_create_picking(self):
        stock_picking_type = request.env['stock.picking.type'].sudo().search([['sequence_code','=','fsm.orders.transfers'],['code','=','outgoing']], limit=1)
        if(not stock_picking_type):
            raise Warning('El tipo de recogida de la transferencia con código fsm.orders.transfers para despachos no se encontro.')

        stock_location_origin = request.env['stock.location'].sudo().search([['fsm_input_type','=','dispatch'], ['usage','=','internal']], limit=1)
        if(not stock_location_origin):
            raise Warning('La ubicación de recogida de la transferencia para despachos no se encontro.')

        stock_location_destination = request.env['stock.location'].sudo().search([['fsm_input_type','=','dispatch'], ['usage','=','customer']], limit=1)
        if(not stock_location_destination):
            raise Warning('La ubicación de recogida de la transferencia para despachos no se encontro.')

        try:
            stock_picking_vals = {
                                    'picking_type_id': int(stock_picking_type.id),
                                    'fsm_order': int(self.id),
                                    'origin': str(self.name),
                                    'location_id': int(stock_location_origin.id),
                                    'location_dest_id': int(stock_location_destination.id),
                                 }

            _logger.warning('stock_picking_vals')
            _logger.warning(stock_picking_vals)

            new_stock_picking = request.env['stock.picking'].sudo().create(stock_picking_vals)
            if(new_stock_picking):
                item_contect = {
                                    'search_default_picking_type_id': int(new_stock_picking.id),
                                    'fsm_order': int(self._origin.id)
                                }
                context = dict(self.env.context)
                context.update(item_contect)

                return {
                            'name': _('Recogida de Pedido de Trabajo'),
                            'view_mode': 'form',
                            'res_model': 'stock.picking',
                            'res_id': new_stock_picking.id,
                            'type': 'ir.actions.act_window',
                            'context': context,
                        }
        except Exception as e:
            _logger.warning("action_create_picking")
            _logger.warning(getattr(e, 'message', repr(e))+" ON LINE "+format(sys.exc_info()[-1].tb_lineno))
            raise Warning('La Recogida de Pedido de Trabajo no se pudo crear.')            

    @api.onchange("partner_account")
    def oc_partner_account(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'partner_channel' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('_onchange_partner_channel')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó la cuenta del pedido a ') + str(self.partner_account.name)  
                self.action_send_notification('partner_account', message)

    @api.onchange("partner_channel")
    def oc_partner_channel(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'partner_channel' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_partner_channel')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el canal a ') + str(self.partner_channel.name)
                self.action_send_notification('partner_channel', message)

    @api.onchange("service_id")
    def oc_service_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'service_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_service_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el servicio a ') + str(self.service_id.name)
                self.action_send_notification('service_id', message)

    @api.onchange("subservice_id")
    def oc_subservice_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'subservice_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_subservice_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el subservicio a ') + str(self.subservice_id.name)
                self.action_send_notification('subservice_id', message)

    @api.onchange("code_merchant")
    def oc_code_merchant(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'code_merchant' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_code_merchant')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el código comerciante a ') + str(self.code_merchant)
                self.action_send_notification('code_merchant', message)
    
    @api.onchange("payment_type_id")
    def oc_payment_type_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'payment_type_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_payment_type_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el tipo de pago a ') + str(self.payment_type_id.name)
                self.action_send_notification('payment_type_id', message)
    
    def return_priority(self,dic_priority,priority):
        for x in dic_priority:
            if priority == x:
                return dic_priority[x]

    @api.onchange("priority")
    def oc_priority(self):
        dic_priority = {'0':'Normal','1':'Bajo','2':'Alto','3':'Urgente'}
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'priority' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_priority')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó la prioridad a ') + str(self.return_priority(dic_priority,self.priority))
                self.action_send_notification('priority', message)
    
    @api.onchange("shipping_type_id")
    def oc_shipping_type_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'shipping_type_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_shipping_type_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el tipo envío del pedido a ') + str(self.shipping_type_id)
                self.action_send_notification('shipping_type_id', message)
    
    @api.onchange("by_package_id")
    def oc_by_package_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'by_package_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_by_package_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el tipo de bulto del pedido a ') + str(self.by_package_id.name)
                self.action_send_notification('by_package_id', message)
    
    @api.onchange("consigned_id")
    def oc_consigned_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'oc_consigned_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_consigned_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el nombre del consignado a ') + str(self.consigned_id.name)
                self.action_send_notification('consigned_id', message)
    
    @api.onchange("consigned_dni")
    def oc_consigned_dni(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'consigned_dni' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_consigned_dni')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el DNI del consignado a ') + str(self.consigned_dni)
                self.action_send_notification('consigned_dni', message)
    
    @api.onchange("consigned_district")
    def oc_consigned_district(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'consigned_district' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_consigned_district')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el distrito del consignado a ') + str(self.consigned_district)
                self.action_send_notification('consigned_district', message)
    
    @api.onchange("consigned_movil")
    def oc_consigned_movil(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'consigned_movil' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_consigned_movil')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el movil del consignado a ') + str(self.consigned_movil)
                self.action_send_notification('consigned_movil', message)
    
    @api.onchange("consigned_mail")
    def oc_consigned_mail(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'consigned_mail' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_consigned_mail')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el correo del consignado a ') + str(self.consigned_mail)
                self.action_send_notification('consigned_mail', message)
    
    @api.onchange("operator_type_id")
    def oc_operator_type_id(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'operator_type_id' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_operator_type_id')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el tipo de operador a ') + str(self.operator_type_id)
                self.action_send_notification('operator_type_id', message)
    
    @api.onchange("service_amount")
    def oc_service_amount(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'service_amount' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_service_amount')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó el monto del servicio a ') + str(self.service_amount)
                self.action_send_notification('service_amount', message)
    
    @api.onchange("appointment_time_from")
    def oc_appointment_time_from(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'appointment_time_from' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_appointment_time_from')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó la hora inicio de la cita a ') + str(self.appointment_time_from)
                self.action_send_notification('appointment_time_from', message)
    
    @api.onchange("appointment_time_until")
    def oc_appointment_time_until(self):
        _model_id = self.env['ir.model'].sudo().search( [ ( 'model', '=', 'fsm.order' ) ]  , limit=1)
        _field_id = self.env['ir.model.fields'].sudo().search( [ ( 'name', '=', 'appointment_time_until' ), ( 'model_id', 'in', [ int(_model_id.id) ] ) ] , limit=1)

        _logger.warning('oc_appointment_time_until')
        _logger.warning(_model_id)
        _logger.warning(_field_id)

        if( _model_id and _field_id ):
            notification_allowed = self.notification_allowed( [ int(_model_id.id) ] , _field_id.ids )
            _logger.warning(notification_allowed)
            if( notification_allowed ):
                message = str('Se actualizó la hora final de la cita a ') + str(self.appointment_time_until)
                self.action_send_notification('appointment_time_until', message)
    
    def action_cancel(self):
        response = super(FsmOrder, self).action_cancel()
        message = str("El pedido de trabajo ( ") + str(self.name) + str(" ) fue cancelado.")
        self.action_send_notification('stage_id', message)
        return response
    
    def action_complete(self):
        response = super(FsmOrder, self).action_complete()
        message = str("El pedido de trabajo ( ") + str(self.name) + str(" ) fue completado.")
        self.action_send_notification('stage_id', message)
        return response

    def action_send_notification(self, _record_name, message=None):
        receivers = []
        receivers_address = []
        
        if(self.person_ids):
            for worker in self.person_ids:
                _logger.warning(worker.partner_id._origin.email)
                receivers.append(worker.partner_id._origin.id)
                if(worker.partner_id._origin.email):
                    receivers_address.append(worker.partner_id._origin.email)
            pass
        if(self.partner_account):
            receivers.append(self.partner_account._origin.id)
            if(self.partner_account._origin.email):
                _logger.warning(self.partner_account._origin.email)
                receivers_address.append(self.partner_account._origin.email)
            pass
        if(self.partner_channel):
            receivers.append(self.partner_channel._origin.id)
            if(self.partner_channel._origin.email):
                _logger.warning(self.partner_channel._origin.email)
                receivers_address.append(self.partner_channel._origin.email)
            pass

        _logger.warning('receivers_address')
        _logger.warning(receivers_address)

        _logger.warning('receivers action_send_notification')
        _logger.warning(receivers)

        mail_message_values =  {
                                    'email_from': self.env.user.partner_id.email,
                                    'author_id': self.env.user.partner_id.id,
                                    'model': 'fsm.order',
                                    'message_type': 'email',
                                    'body': str(message),
                                    'res_id': self._origin.id,
                                    'subtype_id': self.env.ref('mail.mt_comment').id,
                                    'record_name': _record_name,
                                    'moderator_id': self.env.user.partner_id.id, 
                                    'reply_to': str(self.env.user.partner_id.email)
                                }
        
        mail_server = self.env['ir.mail_server'].search([['name','=','Savar']], limit=1)
        if(mail_server):
            mail_message_values['mail_server_id'] = int(mail_server.id)
        
        if(len(receivers)>0):
            mail_message_values['partner_ids'] = [(6, 0, receivers)]

        _logger.warning('mail_message_values')
        _logger.warning(mail_message_values)

        self.env['mail.message'].sudo().create(mail_message_values)        

        mail_values = {
                        'subject': 'Orden de Trabajo actualizado',
                        'body_html': str(message),
                        'email_to':';'.join(map(lambda x: x, receivers_address)),
                        'email_cc':';'.join(map(lambda x: x, receivers_address)),
                        'email_from': self.env.user.partner_id.email,
                      }

        _logger.warning('mail_values')
        _logger.warning(mail_values)

        create_and_send_email = self.env['mail.mail'].create(mail_values).send()