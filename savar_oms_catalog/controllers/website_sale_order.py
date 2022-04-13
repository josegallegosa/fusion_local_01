# -*- coding: utf-8 -*-
from odoo import http
from odoo import models, fields, _
from odoo.http import request
from werkzeug.utils import redirect
from datetime import datetime
from odoo.addons.web.controllers.main import serialize_exception,content_disposition
import xlrd, xlwt
import os
import sys
import logging
import base64
import xlsxwriter
_logger = logging.getLogger(__name__)

class website_sale_order(http.Controller):

    @http.route(['/orders/massive_export_xls_fsm'], type='http', auth='public', methods=['POST'], website=True)
    def massive_export_xlsx_fsm(self, **post):
        sequence_name = request.env["ir.sequence"].next_by_code("xls.pedido.mercantil")
        default_xls = os.path.dirname(os.path.abspath(__file__)) + str('/xls/export.xlsx')        
        default_save_xls = os.path.dirname(os.path.abspath(__file__)) + '/xls/' + str(sequence_name) + str('.xlsx')
        workbook = xlsxwriter.Workbook(default_xls)
        worksheet = workbook.add_worksheet()
        headers = []

        consigned_id = post.get('consigned_id')
        if(bool(consigned_id)):
            headers.append('FSM/Order/Location/Contacto Primario')
        code_merchant = post.get('code_merchant')
        if(bool(code_merchant)):
            headers.append('FSM/Order/Orden comerciante')
        partner_account = post.get('partner_account')
        if(bool(partner_account)):
            headers.append('FSM/Order/Cuenta')
        partner_channel = post.get('partner_channel')
        if(bool(partner_channel)):
            headers.append('FSM/Order/Canal')
        service_id = post.get('service_id')
        if(bool(service_id)):
            headers.append('FSM/Order/Servicio/Name')
        subservice_id = post.get('subservice_id')
        if(bool(subservice_id)):
            headers.append('FSM/Order/Subservicio/Name')
        location_id = post.get('location_id')
        if(bool(location_id)):
            headers.append('FSM/Order/Location')
        scheduled_date_start = post.get('scheduled_date_start')
        if(bool(scheduled_date_start)):
            headers.append('FSM/Order/Despacho/Fecha Inicio')
        partner_channel_street = post.get('partner_channel_street')
        if(bool(partner_channel_street)):
            headers.append('FSM/Order/Canal/Calle')
        partner_channel_district = post.get('partner_channel_district')
        if(bool(partner_channel_district)):
            headers.append('FSM/Order/Canal/Districto')
        partner_channel_mobile = post.get('partner_channel_mobile')
        if(bool(partner_channel_mobile)):
            headers.append('FSM/Order/Canal/Movil')

        row = 0
        col = 0
        
        for item in (headers):
            worksheet.write(row, col, item)
            col += 1

        workbook.close()

        binary_file = open(default_xls, "rb").read()

        request.env['xlsx.templates'].sudo().create({
                                                        'name': str(sequence_name)+str('.xlsx'),
                                                        'xlsx_file': binary_file,
                                                    })

        filecontent = base64.b64decode(binary_file or '')
        content_type, disposition_content = False, False

        content_type = ('Content-Type', 'application/vnd.ms-excel')
        disposition_content = ('Content-Disposition', content_disposition(default_xls))
        return request.make_response(filecontent, [content_type, disposition_content])    

    @http.route(['/orders/massive_save_fsm'], type='http', auth='public', methods=['POST'], website=True)
    def orders_massive_save_fsm(self, **post):
        _orders = []
        
        name = post.get('attachment').filename      
        file = post.get('attachment')
        excel_data = file.read()
        book = xlrd.open_workbook(file_contents=excel_data)
        _logger.warning("****************************************************")
        _logger.warning("EXCEL FILE")
        _logger.warning("-------------------")
        _logger.warning(name)
        _logger.warning("-------------------")

        # fms order collection
        fms_orders = []
        is_line = False
        for worksheet in book.sheets():
            first_row = []
            for col in range(worksheet.ncols):
                first_row.append( worksheet.cell_value(0,col) )
            
            for row in range(1, worksheet.nrows):
                fsm_order = None
                values = {}
                elm = {}
                for col in range(worksheet.ncols):
                    elm[first_row[col]] = worksheet.cell_value(row,col)
                _logger.warning("worksheet elm")
                _logger.warning(elm)
                
                if('FSM/Order/Location' in elm):
                    _logger.warning("cond #1") 
                    if(len(str(elm['FSM/Order/Location'])) > 0):
                        _logger.warning("orders_massive_save_fsm #1 elm")
                        _logger.warning(elm)
                        fms_order = self.create_fms_order(elm)
                        if(fms_order):
                            _logger.warning("-------------------")
                            _logger.warning("ORDER FMS created")
                            _logger.warning(fms_order.id)
                            _logger.warning(fms_order.name)
                            _logger.warning("-------------------")
                    else:
                        _logger.warning("orders_massive_save_fsm #2 elm")
                        _logger.warning(elm)
                        _logger.warning('fsm_order')
                        _logger.warning(fsm_order)
                        domain = []
                        
                        if('FSM/Order/Nombre' in elm):

                            domain = [
                                        ['name', '=', str(elm['FSM/Order/Nombre'])]
                                     ]

                            # request.env.cr.rollback()
                            fsm_order = request.env['fsm.order'].sudo().search(domain, limit=1) 

                        if('FSM/Order/Orden comerciante' in elm):

                            domain = [
                                        ['code_merchant', '=', str(elm['FSM/Order/Orden comerciante'])]
                                     ]

                            # request.env.cr.rollback()
                            fsm_order = request.env['fsm.order'].sudo().search(domain, limit=1)   
                                         
                        
                        product = None
                        domain = []
                        if('FSM/Order/Inventario/Producto/Nombre' in elm):
                            if(len(elm['FSM/Order/Inventario/Producto/Nombre']) > 0):
                                domain.append(['name', '=', str(elm['FSM/Order/Inventario/Producto/Nombre'])])
                        if('FSM/Order/Inventario/Producto/Referencia Interna' in elm):
                            if(len(elm['FSM/Order/Inventario/Producto/Referencia Interna']) > 0):
                                domain.append(['default_code', '=', str(elm['FSM/Order/Inventario/Producto/Referencia Interna'])])                        
                        if('FSM/Order/Inventario/Producto/Marca' in elm):
                            if(len(elm['FSM/Order/Inventario/Producto/Marca']) > 0):
                                domain.append(['product_brand', '=', str(elm['FSM/Order/Inventario/Producto/Marca'])])
                        if('FSM/Order/Inventario/Producto/Modelo' in elm):
                            if(len(elm['FSM/Order/Inventario/Producto/Modelo']) > 0):
                                domain.append(['product_model', '=', str(elm['FSM/Order/Inventario/Producto/Modelo'])])
                        if('FSM/Order/Inventario/Producto/Color' in elm):
                            if(len(elm['FSM/Order/Inventario/Producto/Color']) > 0):
                                domain.append(['product_color', '=', str(elm['FSM/Order/Inventario/Producto/Color'])])
                        
                        if('FSM/Order/Inventario/Producto/Largo' in elm):
                            if(str(elm['FSM/Order/Inventario/Producto/Largo']) != ''):
                                domain.append(['product_length', '=', float(elm['FSM/Order/Inventario/Producto/Largo'])])
                        if('FSM/Order/Inventario/Producto/Ancho' in elm):
                            if(str(elm['FSM/Order/Inventario/Producto/Ancho']) != ''):
                                domain.append(['product_width', '=', float(elm['FSM/Order/Inventario/Producto/Ancho'])])
                        if('FSM/Order/Inventario/Producto/Alto' in elm):
                            if(str(elm['FSM/Order/Inventario/Producto/Alto']) != ''):
                                domain.append(['product_high', '=', float(elm['FSM/Order/Inventario/Producto/Alto'])])
                        
                        _logger.warning("*************")
                        _logger.warning('PRODUCT DOMAIN SEARCH')
                        _logger.warning(domain)                        
                        _logger.warning("*************")
                        product = request.env['product.template'].sudo().search(domain, limit=1)
                        _logger.warning(product)
                        
                        location_id = None
                        domain = []
                        if('FSM/Order/Inventario/Producto/Desde' in elm):
                            if(len(elm['FSM/Order/Inventario/Producto/Desde']) > 0):
                                domain.append(['name', '=', str(elm['FSM/Order/Inventario/Producto/Desde'])])
                                location_id = request.env['stock.location'].sudo().search(domain, limit=1)

                        if(fsm_order):
                            stock_move = {}
                            stock_moves = []
                            if(product):
                                stock_move['product_id'] = int(product.id)
                            if(location_id):
                                stock_move['location_id'] = int(location_id.id)

                            if('FSM/Order/Inventario/Producto/Desde' in elm):
                                if(len(elm['FSM/Order/Inventario/Producto/Desde']) > 0):
                                    stock_move['quantity'] = int(elm['FSM/Order/Inventario/Producto/Cantidad'])
                            
                            if('FSM/Order/Inventario/Producto/Bulto' in elm):
                                if(len(elm['FSM/Order/Inventario/Producto/Bulto']) > 0):
                                    stock_move['package_lump'] = str(elm['FSM/Order/Inventario/Producto/Bulto'])

                            stock_moves.append(stock_move)
                            _logger.warning("orders_massive_save_fsm #1 is_line")
                            _logger.warning(is_line)
                            request.env['fsm.order'].sudo().create_fms_order_inventory(stock_moves, fsm_order)
        
        url_redirection = post.get("url_redirection")
        if(url_redirection):
            return redirect(url_redirection)
        return redirect("/my/fsm_orders")

    @http.route(['/orders/massive_save'], type='http', auth='public', methods=['POST'], website=True)
    def orders_massive_save(self, **post):
        _logger.warning('orders_massive_save')
        _logger.warning(post)
        _orders = []
        
        name = post.get('attachment').filename      
        file = post.get('attachment')
        excel_data = file.read()
        book = xlrd.open_workbook(file_contents=excel_data)
        _logger.warning("****************************************************")
        _logger.warning("EXCEL FILE")
        _logger.warning("-------------------")
        _logger.warning(name)
        _logger.warning("-------------------")

        partner_id = None
        partner_id_delivery = None
        partner_id_invoice = None
        lines = []
        current_same_order = None
        last_sequence = None
        add_as_line = False

        # fms order collection
        fms_orders = []

        for worksheet in book.sheets():
            first_row = []
            for col in range(worksheet.ncols):
                first_row.append( worksheet.cell_value(0,col) )
            data =[]
            for row in range(1, worksheet.nrows):
                lines = []
                values = {}
                elm = {}                
                for col in range(worksheet.ncols):
                    elm[first_row[col]]=worksheet.cell_value(row,col)
                data.append(elm)
                # save time: while collecting data will process
                if('Referencia del pedido' in elm):
                    _logger.warning("add_as_line comparation")
                    _logger.warning(str(elm['Referencia del pedido']))
                    _logger.warning(str(last_sequence))
                    if(last_sequence==None):
                        _logger.warning("****** &")
                        values['sequence'] = elm['Referencia del pedido']
                        last_sequence = elm['Referencia del pedido']
                        add_as_line = False
                    elif(len(last_sequence)>0):
                                                
                        if( str(last_sequence) == str(elm['Referencia del pedido'])):
                            add_as_line = True
                            _logger.warning("****** $ 1")
                        else:
                            _logger.warning("****** $ 1")
                            add_as_line = False
                        values['sequence'] = elm['Referencia del pedido']
                        last_sequence = elm['Referencia del pedido']
                    else:
                        values['sequence'] = elm['Referencia del pedido']                        
                        if( str(last_sequence) == str(elm['Referencia del pedido'])):
                            last_sequence = elm['Referencia del pedido']
                            add_as_line = True
                            _logger.warning("****** $")                        
                
                _logger.warning("add_as_line ")
                _logger.warning(add_as_line)

                # No operar con campos para lineas vacios en excel
                if(add_as_line==False):
                    pass                                     
                
                if('Tipo' in elm):
                    if(elm['Tipo'] == 'pedido'):
                        # Buscar cliente por nombre, vat
                        _domain = []
                        if('Cliente/Nombre' in elm or 'Cliente/NIF' in elm):
                            _domain = ['|']
                            if(elm['Cliente/Nombre']):
                                _domain.append(['name', '=', elm['Cliente/Nombre']])
                            if(elm['Cliente/NIF']):
                                _domain.append(['vat', '=', elm['Cliente/NIF']])   
                            _domain = self.clean_operator(_domain,'|')                                           
                        elif('Cliente/Nombre' in elm and 'Cliente/NIF' in elm):
                            _domain = [
                                        ['name', '=', elm['Cliente/Nombre']],
                                        ['vat', '=', elm['Cliente/NIF']]
                                      ]
                        else:
                            pass
                        
                        _logger.warning("Buscar cliente por nombre, vat _domain")
                        _logger.warning(_domain)
                        partner_id = request.env['res.partner'].sudo().search(_domain, limit=1)
                        if(partner_id):
                            values['partner_id'] = int(partner_id.id)
                        else:
                            partner_vals = {
                                                'vat': str(elm['Cliente/NIF']),
                                                'name': str(elm['Cliente/Nombre']),
                                                'email': str(elm['Cliente/CorreoElectronico']),
                                                'street': str(elm['Cliente/Direccion']),
                                            }
                            partner_id = request.env['res.partner'].sudo().create(partner_vals)
                            values['partner_id'] = int(partner_id.id)
                            # update ubigeo
                            self.update_partner_ubigeo(partner_id, str(elm['Cliente/Ubigeo']))

                        _logger.warning("Cliente")
                        _logger.warning(partner_id.id)
                        _logger.warning(partner_id.name)

                        # Buscar direccion factura cliente por nombre, vat
                        _domain = []
                        if('Dirección de factura/Nombre' in elm or 'Dirección de factura/NIF' in elm):
                            _domain = ['|']
                            if(elm['Dirección de factura/Nombre']):
                                _domain.append(['name', '=', elm['Dirección de factura/Nombre']])
                            if(elm['Dirección de factura/NIF']):
                                _domain.append(['vat', '=', elm['Dirección de factura/NIF']])                                                
                            _domain = self.clean_operator(_domain,'|')
                        elif('Dirección de factura/Nombre' in elm and 'Dirección de factura/NIF' in elm):
                            _domain = [
                                        ['name', '=', elm['Dirección de factura/Nombre']],
                                        ['vat', '=', elm['Dirección de factura/NIF']]
                                      ]
                        else:
                            pass

                        _logger.warning("Buscar direccion factura cliente _domain")
                        _logger.warning(_domain)
                        partner_invoice_id = request.env['res.partner'].sudo().search(_domain, limit=1)
                        _domain = []
                        if(partner_invoice_id):
                            values['partner_invoice_id'] = int(partner_invoice_id.id)
                            _logger.warning("Cliente Factura")
                            _logger.warning(partner_invoice_id.id)
                            _logger.warning(partner_invoice_id.name)
                        else:
                            partner_vals = {
                                                'vat': str(elm['Dirección de entrega/NIF']),
                                                'name': str(elm['Dirección de entrega/Nombre']),
                                                'email': str(elm['Dirección de entrega/CorreoElectronico']),
                                                'street': str(elm['Dirección de entrega/Direccion']),
                                            }
                            partner_invoice_id = request.env['res.partner'].sudo().create(partner_vals)
                            values['partner_invoice_id'] = int(partner_invoice_id.id)
                            # update ubigeo
                            self.update_partner_ubigeo(partner_invoice_id, str(elm['Dirección de entrega/Ubigeo']))
                        
                        # Buscar direccion entrega cliente por nombre, vat
                        _domain = []
                        if('Dirección de entrega/Nombre' in elm or 'Dirección de entrega/NIF' in elm):
                            _domain = ['|']
                            if(elm['Dirección de entrega/Nombre']):
                                _domain.append(['name', '=', elm['Dirección de entrega/Nombre']])
                            if(elm['Dirección de entrega/NIF']):
                                _domain.append(['vat', '=', elm['Dirección de entrega/NIF']])
                            _domain = self.clean_operator(_domain,'|')                                            
                        elif('Dirección de entrega/Nombre' in elm and 'Dirección de entrega/NIF' in elm):
                            _domain = [
                                        ['name', '=', elm['Dirección de entrega/Nombre']],
                                        ['vat', '=', elm['Dirección de entrega/NIF']]
                                    ]             
                        else:
                            pass
                        
                        _logger.warning("Buscar direccion entrega cliente por nombre, vat _domain")
                        _logger.warning(_domain)
                        partner_delivery_id = request.env['res.partner'].sudo().search(_domain, limit=1)
                        _domain = []
                        if(partner_delivery_id):
                            values['partner_delivery_id'] = int(partner_delivery_id.id)
                            _logger.warning("Cliente")
                            _logger.warning(partner_delivery_id.id)
                            _logger.warning(partner_delivery_id.name)   

                            values['lines'] = lines
                            # include orders
                            _orders.append(values)
                        else:
                            partner_vals = {
                                                'vat': str(elm['Dirección de factura/NIF']),
                                                'name': str(elm['Dirección de factura/Nombre']),
                                                'email': str(elm['Dirección de factura/CorreoElectronico']),
                                                'street': str(elm['Dirección de factura/Direccion'])
                                            }
                            partner_delivery_id = request.env['res.partner'].sudo().create(partner_vals)
                            values['partner_delivery_id'] = int(partner_delivery_id.id)
                            # update ubigeo
                            self.update_partner_ubigeo(partner_delivery_id, str(elm['Dirección de factura/Ubigeo']))

                    if(elm['Tipo'] == 'linea'):
                        # *** BG COLECION PARA LINEA
                        _line = {}                

                        # Parent service
                        service_name = str(elm['Líneas de Pedido/SubServicios/Parent Service'])
                        service = request.env['fsm.order.service'].sudo().search([['name', '=', str(service_name)]], limit=1)
                        if(service):
                            _logger.warning("Service")
                            _logger.warning(service.id)
                            subservice_name = str(elm['Líneas de Pedido/SubServicios/Name'])
                            subservice = request.env['fsm.order.service'].sudo().search([['name', '=', str(subservice_name)], ['parent_id', '=', int(service.id)]], limit=1)
                            if(subservice):
                                _line['product_subservice'] = int(subservice.id)  
                        # Buscar producto por referencia interna o codigo de barras
                        _domain = []
                        if('Líneas de Pedido/Producto/Referencia Interna' in elm or 'Líneas de Pedido/Producto/Código de Barras' in elm):
                            _domain = ['|']
                            if(elm['Líneas de Pedido/Producto/Referencia Interna']):
                                _domain.append(['default_code', '=', elm['Líneas de Pedido/Producto/Referencia Interna']])
                            if(elm['Líneas de Pedido/Producto/Código de Barras']):
                                _domain.append(['barcode', '=', elm['Líneas de Pedido/Producto/Código de Barras']])                                                
                            _domain = self.clean_operator(_domain,'|')
                        elif('Líneas de Pedido/Producto/Referencia Interna' in elm and 'Líneas de Pedido/Producto/Código de Barras' in elm):
                            _domain = [
                                        ['barcode', '=', elm['Líneas de Pedido/Producto/Código de Barras']],
                                        ['default_code', '=', elm['Líneas de Pedido/Producto/Referencia Interna']]
                                      ]
                        else:
                            pass                
                        
                        _logger.warning("Buscar producto _domain")
                        _logger.warning(_domain)
                        product_template = request.env['product.template'].sudo().search(_domain, limit=1)
                        _domain = []
                        if(product_template):
                            _line['product_id'] = int(product_template.id)
                            _logger.warning("Producto")
                            _logger.warning(product_template.id)
                            _logger.warning(product_template.name)
                            
                        _line['product_quantity'] = str(elm['Líneas de Pedido/Cantidad'])
                        _line['product_description'] = str(elm['Líneas de Pedido/Producto/Nombre'])
                        
                        __order = _orders[int(len(_orders)-int(1))]
                        _logger.warning('__order')
                        _logger.warning(__order)
                        __lines = __order['lines']
                        __lines.append(_line)
                        __order['lines'] = __lines
                        try:
                            _line['product_price'] = float(elm['Líneas de Pedido/Precio unitario'])
                        except:
                            _line['product_price'] = float(0.0)
                            pass
                        _line['product_taxes'] = None

                    #if(elm['Tipo'] == 'fms'):
                    #    fms_orders.append(elm)                                       
                    
                _logger.warning("-------------------")
                _logger.warning("ORDER DATA")
                _logger.warning("-------------------")
                _logger.warning(values)
                # eof coleccion info pedido                

            _logger.warning("-------------------")
            _logger.warning("ORDERs LIST")
            _logger.warning("-------------------")
            _logger.warning(_orders)
        
            _logger.warning("-------------------")
            _logger.warning("SHEET VECTOR DATA")
            _logger.warning("-------------------")
            _logger.warning(data)
        
        if(_orders):
            for order in _orders:
                ___order = request.env['sale.order'].sudo().search([['name', '=', str(order['sequence'])]])
                if(___order):
                    order_id = int(___order.id)
                else:
                    order_id = int(0)
                self.order_create(order_id, order['sequence'], order['partner_id'], order['partner_invoice_id'], order['partner_delivery_id'], order['lines'])

        # add fms order
        if(fms_orders):
            if( len(fms_orders)>0 ):
                for _fms_order in fms_orders:
                    fms_order = self.create_fms_order(_fms_order)
                    if(fms_order):
                        _logger.warning("-------------------")
                        _logger.warning("ORDER FMS created")
                        _logger.warning(fms_order.id)
                        _logger.warning(fms_order.name)
                        _logger.warning("-------------------")

        _logger.warning("****************************************************")

        response = redirect("/my/merchant_orders")
        return response
    
    def update_partner_ubigeo(self, partner, ubigeo):
        if(partner and ubigeo):
            location = str(ubigeo).split('|')
            if( len(location)>0 ):
                _logger.warning('update_partner_ubigeo location')
                _logger.warning(location)
                if(location):
                    location_state = None
                    location_province = None
                    location_district = None                    
                    if(len(location)==3):
                        location_state = str(location[0]).strip()
                        location_province = str(location[1]).strip()
                        location_district = str(location[2]).strip()

                    _logger.warning(str('state: ')+str((location_state)))
                    _logger.warning(str('province: ')+str((location_province)))
                    _logger.warning(str('district: ')+str((location_district)))

                    state_id = request.env['res.country.state'].sudo().search([
                                                                                ['name', '=', location_state],
                                                                                ['province_id', '=', None],
                                                                                ['state_id', '=', None],
                                                                            ], limit=1)
                    _logger.warning('state_id')
                    _logger.warning(state_id.name)
                    _logger.warning(state_id.country_id.name)
                    
                    province_id = request.env['res.country.state'].sudo().search([
                                                                                    ['name', '=', location_province],
                                                                                    ['province_id', '=', None],
                                                                                    ['state_id', '!=', None]
                                                                                ], limit=1)
                    _logger.warning('province_id')
                    _logger.warning(province_id.name)

                    
                    country_id = request.env['res.country'].sudo().browse(int(state_id.country_id.id))
                    _logger.warning('country_id')
                    _logger.warning(country_id.name)
                    
                    district_id = request.env['res.country.state'].sudo().search([
                                                                                    ['name', '=', str(location_district)],
                                                                                    ['province_id', '=', int(province_id.id)],
                                                                                    ['state_id', '=', int(state_id.id)],
                                                                                    ['country_id', '=', int(country_id.id)],
                                                                                 ], limit=1)
                    _logger.warning('district_id')
                    _logger.warning(district_id.name)

                    partner.sudo().update({
                                            'country_id': int(country_id.id),
                                            'state_id': int(state_id.id),
                                            'province_id': int(province_id.id),
                                            'district_id': int(district_id.id),
                                          })

    def clean_operator(self, domain, oparator):
        _domain = []
        if(domain):
            _logger.warning('BG clean_operator')
            _logger.warning(domain)
            _logger.warning(len(domain))
            if(len(domain)==int(2)):
                _domain.append(domain[1])
                _logger.warning('END clean_operator')
                _logger.warning(_domain)
                return _domain                        
        return domain

    def create_fms_order(self, elm):
        _logger.warning('create_fms_order')
        _logger.warning(elm)
        values = {}
        fsm_order = None
        sequence = request.env['ir.sequence'].next_by_code('fsm.order')        
        if(sequence):
            elm['FSM/Order/Nombre'] = sequence
            values['name'] = elm['FSM/Order/Nombre']
            if('FSM/Order/Nombre de Etapa' in elm):
                _domain = [
                            ['name', '=', elm['FSM/Order/Nombre de Etapa']],
                            ['stage_type', '=', 'order'],
                          ]
                          
                _logger.warning('FSM/Order/Nombre de Etapa')
                _logger.warning(_domain)

                stage = request.env['fsm.stage'].sudo().search(_domain, limit=1)
                if(stage):
                    values['stage_id'] = int(stage.id)
            
            if('FSM/Order/Subetapa' in elm):
                _domain = [
                            ['name', '=', elm['FSM/Order/Subetapa']],
                          ]
                          
                _logger.warning('FSM/Order/Nombre de Subetapa')
                _logger.warning(_domain)

                substage = request.env['fsm.stage.status'].sudo().search(_domain, limit=1)
                if(substage):
                    values['sub_stage_id'] = int(substage.id)

            if('FSM/Order/Servicio/Name' in elm):
                service_name = elm['FSM/Order/Servicio/Name']
                # Parent service
                service = request.env['fsm.order.service'].sudo().search([['name', '=', str(service_name)]], limit=1)            
                if(service):
                    values['service_id'] = int(service.id)
                    subservice_name = str(elm['FSM/Order/Subservicio/Name'])
                    subservice = request.env['fsm.order.service'].sudo().search([['name', '=', str(subservice_name)], ['parent_id', '=', int(service.id)]], limit=1)
                    if(subservice):
                        values['subservice_id'] = int(subservice.id)   

            if('FSM/Order/Instrucciones' in elm):
                values['todo'] = str(elm['FSM/Order/Instrucciones'])  

            if('FSM/Order/Descripcion' in elm):
                values['description'] = str(elm['FSM/Order/Descripcion'])           
            
            if('FSM/Order/Prioridad' in elm):
                priority = str(0)
                if(str(elm['FSM/Order/Prioridad'])=="Bajo"):
                    priority =  str(1)
                if(str(elm['FSM/Order/Prioridad'])=="Alto"):
                    priority =  str(2)
                elif(str(elm['FSM/Order/Prioridad'])=="Urgente"):
                    priority =  str(3)
                else:
                    priority = str(0)
                #values['priority'] = str(priority)           

            # used in primary contact below this condiction
            location = None
            if('FSM/Order/Location' in elm):
                _domain = [
                            ['ref', '=', elm['FSM/Order/Location']],
                            #['stage_type', '=', 'order'],
                          ]
                          
                _logger.warning('FSM/Order/Location')
                _logger.warning(_domain)

                location = request.env['fsm.location'].sudo().search(_domain, limit=1)
                _logger.warning(location)
                if(location):
                    values['location_id'] = int(location.id)
                
                    if('FSM/Order/Location/Movil' in elm):
                        if(len((str(elm['FSM/Order/Location/Movil'])))>0):
                            location.sudo().update({
                                                        'phone':str(elm['FSM/Order/Location/Movil'])
                                                    })
                    if('FSM/Order/Location/Correo Electronico' in elm):
                        if(len((str(elm['FSM/Order/Location/Correo Electronico'])))>0):
                            location.sudo().update({
                                                        'email':str(elm['FSM/Order/Location/Correo Electronico'])
                                                    })
                    if('FSM/Order/Location/Calle' in elm):
                        if(len((str(elm['FSM/Order/Location/Calle'])))>0):
                            location.sudo().update({
                                                        'street2':str(elm['FSM/Order/Location/Calle'])
                                                    })
                                                                
                    if('FSM/Order/Location/Contacto Primario' in elm):
                        _domain = [
                                    ['name', '=', elm['FSM/Order/Location/Contacto Primario']],
                                    ['type', '=', 'contact']
                                ]
                                
                        _logger.warning('FSM/Order/Location/Contacto Primario')
                        _logger.warning(_domain)
                        _partner = request.env['res.partner'].sudo().search(_domain)
                        if(_partner and location):
                            location.sudo().update({'contact_id':int(_partner)})
            
            if('FSM/Order/Orden comerciante' in elm):
                values['code_merchant'] = str(elm['FSM/Order/Orden comerciante'])

            if('FSM/Order/Medio de Pago/Nombre' in elm):
                _domain = [
                            ['name', '=', elm['FSM/Order/Medio de Pago/Nombre']],
                          ]
                payment_type_id = request.env['payment.type'].sudo().search(_domain, limit=1)
                if(payment_type_id):
                    values['payment_type_id'] = int(payment_type_id.id)

            if('FSM/Order/Tipo de bulto/Nombre' in elm):
                _domain = [
                            ['name', '=', elm['FSM/Order/Tipo de bulto/Nombre']],
                          ]
                by_package_id = request.env['by.package'].sudo().search(_domain, limit=1)
                if(by_package_id):
                    values['by_package_id'] = int(by_package_id.id)

            if('FSM/Order/Tipo de Transporte' in elm):
                shipping_type = request.env['shipping.type'].sudo().search([['name','=',str(elm['FSM/Order/Tipo de Transporte'])]], limit=1)
                if(shipping_type):
                    values['shipping_type_id'] = int(shipping_type.id)

            if('FSM/Order/Datos del consignado' in elm):
                values['consigned_id'] = str(elm['FSM/Order/Datos del consignado'])

            if('FSM/Order/Inicio de Cita' in elm):
                values['appointment_time_from'] = str(elm['FSM/Order/Inicio de Cita'])

            if('FSM/Order/Fin de la Cita' in elm):
                values['appointment_time_until'] = str(elm['FSM/Order/Fin de la Cita'])
            
            if('FSM/Order/Compañia' in elm):
                company = request.env['res.company'].sudo().search([['name','=',str(elm['FSM/Order/Compañia'])]], limit=1)
                if(company):
                    values['company_id'] = int(company.id)
            
            if('FSM/Order/Cuenta' in elm):
                _domain = [
                            ['name', '=', elm['FSM/Order/Cuenta']],
                          ]
                partner = request.env['res.partner'].sudo().search(_domain, limit=1)
                if(partner):
                    values['partner_account'] = int(partner.id)
                partner= None
            
            if('FSM/Order/Canal' in elm):
                _domain = [
                            ['name', '=', elm['FSM/Order/Canal']],
                          ]
                partner = request.env['res.partner'].sudo().search(_domain, limit=1)
                if(partner):
                    values['partner_channel'] = int(partner.id)
                partner= None

            if('FSM/Order/Despacho/Fecha Inicio' in elm):
                if(str(elm['FSM/Order/Despacho/Fecha Inicio'])!=""):
                    values['scheduled_date_start'] = self.convert_datetime(elm['FSM/Order/Despacho/Fecha Inicio'])
            
            if('FSM/Order/Despacho/Duraccion' in elm):
                if(float(elm['FSM/Order/Despacho/Duraccion'])>0):
                    values['scheduled_duration'] = float(elm['FSM/Order/Despacho/Duraccion'])

            if('FSM/Order/Despacho/Fecha Fin' in elm):
                if(str(elm['FSM/Order/Despacho/Fecha Fin'])!=""):
                    values['scheduled_date_end'] = self.convert_datetime(elm['FSM/Order/Despacho/Fecha Inicio'])
            
            _logger.warning('create_fms_order values')
            _logger.warning(values)

            # BG Create FSM Order
            fsm_order = request.env['fsm.order'].sudo().create(values)
            if(fsm_order):
                if('Referencia del pedido' in elm):
                    _logger.warning("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    _logger.warning("create_fms_order domain")
                    _logger.warning(['name', '=', str(elm['Referencia del pedido'])])

                    sale_order = request.env['sale.order'].sudo().search([
                                                                            ['name', '=', str(elm['Referencia del pedido'])]
                                                                        ])
                    if(sale_order):
                        _logger.warning("create_fms_order sale_order")
                        _logger.warning(sale_order.id)
                        _logger.warning(sale_order.name)
                        fsm_order.sudo().update({'sale_order': int(sale_order.id)})
                        fsm_order_ids = []
                        if(sale_order.fsm_order_ids):
                            for fsm_order in sale_order.fsm_order_ids:
                                fsm_order_ids.append(int(fsm_order.id))
                        
                        fsm_order_ids.append(int(fsm_order.id))
                        sale_order.sudo().update({
                                                    'fsm_order_ids':[(6, 0, fsm_order_ids)],
                                                })

            # EOF Create FSM Order
                    _logger.warning("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return fsm_order  

    def convert_datetime(self, _float):
        try:
            serial = float(_float)
            seconds = (serial - 25569) * 86400.0
            date_time = datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M')
            return date_time
        except:
            return ""
    @http.route(['/orders/get_pricelist'], type='json', auth='public', methods=['POST'], website=True)
    def get_pricelist(self, subservice_id):
        _pricelists = []
        my_merchant_account = request.env.user.partner_id
        _domain = [
                    ['merchant_account', '=', int(my_merchant_account.id)],
                  ]
        
        _logger.warning("***************************")
        _logger.warning("pricelists")        
        _logger.warning(_domain)

        pricelists = request.env['oms.pricelist'].search(_domain)

        _logger.warning(pricelists)
        _logger.warning("***************************")
        if(pricelists):
            for pricelist in pricelists:
                if(subservice_id):
                    _domain = []

                    try:
                        _domain_item = ['subservice_id', '=', int(subservice_id)]
                        _domain.append(_domain_item)
                        _logger.warning("pricelists _domain_item subservice") 
                        _logger.warning(_domain_item) 
                    except:
                        pass

                    _logger.warning("pricelists list ids")        
                    _logger.warning(_domain)

                    pricelists_lines = request.env['oms.pricelist.item'].search(_domain)
                    for pricelists_line in pricelists_lines:
                        item = {
                                    'pricelist_id':int(pricelist.id),
                                    'pricelist_name':str(pricelist.name),
                                    'pricelist_currency':str(pricelist.currency_id.name),
                                    'pricelist_line_id':int(pricelists_line.id),
                                    'pricelist_line_price':format(float(pricelists_line.price), '.2f'),
                                    'pricelist_line_subservice_id':int(pricelists_line.subservice_id.id),
                                    'pricelist_line_subservice_name':str(pricelists_line.subservice_id.name),
                                }
                        _pricelists.append(item)

                _logger.warning("get_pricelist domain")
                _logger.warning(_domain)
        
        _logger.warning("____________________________")
        _logger.warning("get_pricelist")
        _logger.warning(_pricelists)
        _logger.warning("____________________________")
        return _pricelists
          

    @http.route(['/orders/create'], type='json', auth='public', methods=['POST'], website=True)
    def order_create(self, order_id, sequence, partner_id, partner_invoice_id, partner_delivery_id, lines):
        partner = request.env.user.partner_id
        values = {  
                    'name': str(sequence),
                    'partner_id': int(partner_id),
                    'merchant_account': int(partner.id),
                    'partner_invoice_id': int(partner_invoice_id),
                    'partner_shipping_id': int(partner_delivery_id),
                 }
        
        _logger.warning("website_sale_order #########################")
        _logger.warning(values)
        _logger.warning(order_id)

        if(int(order_id) > 0): # edit mode
            order_id = request.env['sale.order'].sudo().browse(int(order_id))
        else: # new one mode
            order_id = request.env['sale.order'].sudo().create(values)

        if(lines):
            for _line in lines:
                _logger.warning('_line')
                _logger.warning(_line)
                _product = request.env['product.product'].sudo().search([
                                                                            ['product_tmpl_id', '=', int(_line['product_id'])]
                                                                        ], limit=1)
                new_line = request.env['sale.order.line'].sudo().create({
                                                                            'product_id': int(_product.id),
                                                                            'name': str(_line['product_description']),
                                                                            'order_id':order_id.id,                                                                            
                                                                            'product_uom_qty': str(_line['product_quantity']),
                                                                            'product_uom' : int(_product.uom_id.id),
                                                                            'price_unit' : float(_line['product_price'])
                                                                        })
                taxes =  _line['product_taxes']
                if(taxes):
                    _taxes_values = []
                    _taxes_ids = str(taxes).split(",")
                    if(_taxes_ids):
                        for _tax in _taxes_ids:
                            _taxes_values.append(int(_tax))
                        _logger.warning('_taxes_values')
                        _logger.warning(_taxes_values)
                        new_line.sudo().update({'tax_id': [[6, 0,_taxes_values]] })

                product_subservice =  _line['product_subservice']
                if(product_subservice):
                    new_line.sudo().update({'subservice_id': product_subservice })
                            
        return request.env['sale.order'].sudo().browse(int(order_id.id)).read()

    @http.route(['/orders/get_values'], type='json', auth='public', methods=['POST'], website=True)
    def get_order_values(self, order_id):
        order = None
        response = []
        if(order_id):
            order = request.env['sale.order'].browse(int(order_id))
            order_lines = []
            if(order):
                response = {
                                'id': order.id,
                                'name': order.name,
                                'partner_invoice_id': order.partner_invoice_id.id,
                                'partner_invoice_name': order.partner_invoice_id.name,
                                'partner_delivery_id': order.partner_shipping_id.id,
                                'partner_delivery_name': order.partner_shipping_id.name,
                                'partner_id': order.partner_id.id,
                                'partner_id_name': order.partner_id.name,
                                'lines': [],
                            }
                if(order.order_line):
                    for line in order.order_line:
                        item =  {
                                    'id': line.id,
                                    'product_id': line.product_id.id,
                                    'product_id_name': line.product_id.name,
                                    'product_description': line.name,
                                    'quantity': line.product_uom_qty,
                                    'unit_price': line.price_unit,
                                    'taxes': self.get_order_values_taxes(line.tax_id),
                                    'subservice_id': line.subservice_id.id,
                                    'subservice_name': line.subservice_id.name,
                                }
                        order_lines.append(item)
                    response['lines'] = order_lines
        response['lines_count'] = len(response['lines'])
        return response                  
    
    def get_order_values_taxes(self, taxes):
        _taxes = []
        if(taxes):
            for tax in taxes:
                item = {'id':tax.id, 'text':tax.name}
                _taxes.append(item)
        return _taxes   