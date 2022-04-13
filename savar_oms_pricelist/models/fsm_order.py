from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class FsmOrder(models.Model):
	_inherit = 'fsm.order'
	
	code_merchant = fields.Char(string='Cod. Orden de trabajo')
	service_id = fields.Many2one('fsm.order.service', string='Servicio')	
	subservice_id = fields.Many2one('fsm.order.service', string='Subservicio')
	
	by_package_id = fields.Many2one('by.package', string='Tipo de bulto')
	payment_type_id = fields.Many2one('payment.type', string='Tipo de Pago')
	shipping_type_id = fields.Many2one("shipping.type", string='Tipo de Transporte')
	operator_type_id = fields.Char(string="Tipo de Operador", related="company_id.operator_type_id.name")
	consigned_id = fields.Char(string='Datos del consignado')
	date_dispatch = fields.Date(string='Fecha de despacho')

	movement_type = fields.Char(string="Tipo Movimiento", default="Despacho", store=True)
	
	appointment_time_from = fields.Selection(
	string="hora cita desde",
		selection=[
			('8_00_am', '08:00 AM'),
			('8_30_am', '08:30 AM'),
			('9_00_am', '09:00 AM'),
			('9_30_am', '09:30 AM'),
			('10_00_am', '10:00 AM'),
			('10_30_am', '10:30 AM'),
			('11_00_am', '11:00 AM'),
			('11_30_am', '11:30 AM'),
			('12_00_am', '12:00 AM'),
			('12_30_am', '12:30 AM'),
			('01_00_am', '01:00 AM'),
			('01_30_am', '01:30 AM'),
			('02_00_am', '02:00 AM'),
			('02_30_am', '02:30 AM'),
			('03_00_am', '03:00 AM'),
			('03_30_am', '03:30 AM'),
			('04_00_am', '04:00 AM'),
			('04_30_am', '04:30 AM'),
			('05_00_am', '05:00 AM'),
			('05_30_am', '05:30 AM'),
			('06_00_am', '06:00 AM'),
			('06_30_am', '06:30 AM'),
			
		], default="8_00_am"
	)

	appointment_time_until = fields.Selection(
		string="hora cita hasta",
		selection=[
			('8_00_am', '08:00 AM'),
			('8_30_am', '08:30 AM'),
			('9_00_am', '09:00 AM'),
			('9_30_am', '09:30 AM'),
			('10_00_am', '10:00 AM'),
			('10_30_am', '10:30 AM'),
			('11_00_am', '11:00 AM'),
			('11_30_am', '11:30 AM'),
			('12_00_am', '12:00 AM'),
			('12_30_am', '12:30 AM'),
			('01_00_am', '01:00 AM'),
			('01_30_am', '01:30 AM'),
			('02_00_am', '02:00 AM'),
			('02_30_am', '02:30 AM'),
			('03_00_am', '03:00 AM'),
			('03_30_am', '03:30 AM'),
			('04_00_am', '04:00 AM'),
			('04_30_am', '04:30 AM'),
			('05_00_am', '05:00 AM'),
			('05_30_am', '05:30 AM'),
			('06_00_am', '06:00 AM'),
			('06_30_am', '06:30 AM'),
			
		], default="8_30_am"
	)

	service_amount = fields.Float(string='Monto del servicio')

	@api.onchange('service_amount')
	def onchange_service_amount(self):
		if self.service_amount<0:
			raise UserError('El monto del servicio no puede ser negativo!!')

	@api.onchange('service_id')
	def onchange_service_id(self):
		_logger.warning("onchange_service_id")
		if(self):
			for record in self:
				
				_logger.warning(record.service_id.name)

				if(record.service_id):	
					_logger.warning("move_ids")
					_logger.warning(record.move_ids)
					for move_id in record.move_ids:
						if(move_id):
							if(record.service_id.name == str("FulFillment")):
								move_id.update({'tree2visibility':False})
							else:
								move_id.update({'tree2visibility':True})
							
							_logger.warning("move_id.tree2visibility")
							_logger.warning(move_id.tree2visibility)

					record.package_lump_ids = None
					record.package_lump_amount = float(0.0)
	
	@api.onchange('stage_id')
	def onchange_stage_id(self):
		_logger.warning("onchange_stage_id")
		monto_total_servicio = float(0)
		if( str(self.stage_id.name) == str("Entregado/Fallido") ):
			price_lists = self.env['oms.pricelist'].sudo().search( [  ] ) # ['service_id', '=', int(self.service_id.id)]
			if(price_lists):

				_logger.warning("price_lists")
				_logger.warning(price_lists)

				for price_list in price_lists:
					_logger.warning("price_list.pricelist_item3_ids")
					_logger.warning(price_list.pricelist_item3_ids)
					if(price_list.pricelist_item3_ids):
						_filter = [['id', 'in', price_list.pricelist_item3_ids.ids]]
						price_lists_items = self.env['oms.pricelist.item'].sudo().search(_filter)

						_logger.warning("price_lists_items")
						_logger.warning(price_lists_items)

					for price_lists_item in price_lists_items:
						if( float(price_lists_item.failed_recount)>0 and float(price_lists_item.failed_amount_charge)>0 ):
							monto_total_servicio = float(price_lists_item.failed_recount) * float(price_lists_item.failed_amount_charge)
							monto_total_servicio = float(monto_total_servicio) + float(price_lists_item.price)
						else:
							_logger.warning("price_lists_item.price")
							_logger.warning(price_lists_item.price)
							monto_total_servicio =  ( monto_total_servicio + price_lists_item.price )
						price_lists_item.sudo().update({ 'failed_recount': ( price_lists_item.failed_recount + 1) })

				self.service_amount = monto_total_servicio