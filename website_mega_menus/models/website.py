
# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
import logging
_logger = logging.getLogger(__name__)
class Menu(models.Model):

	_inherit = "website.menu"
	is_wk_mega_menu = fields.Boolean(
		string="Mega Menu",
		help="Show the categories as a mega menu on this menu",
		readonly=True
	)
	root_category = fields.Many2one(
		comodel_name="product.public.category",
		string="Root Category",
		help="If any root category is not selected then all the categories will be displayed."
	)
	categories_displayed = fields.Selection(
		[('all','ALL'),
		('selected','Selected')],
		string='Categories To Display'
	)
	selected_categories = fields.Many2many(
		'product.public.category','menu_id','category_id','rel',
		string="Select Categories",
	)
	bg_image = fields.Binary(
		string="Background Image",
		help="Image to be displayed on the background of the mega menu"
	)
	top_menu_icon = fields.Binary(
		string="Top Menu Icon",
		help="Icon to be displayed on the top menu of mega menu"
	)

	def create_url(self):
		if self.root_category:
			self.url = "/shop/category/%s" % slug(self.root_category)
		return True

	# @api.model
	# def show_mega_menu_form(self,*args):
	# 	_logger.info("\n.................%r..............",*args)
	# 	current_id = self.ids
	# 	action = self.env.ref('website_mega_menus.action_website_mega_menus_id').read()[0]
	# 	if len(current_id) > 1:
	# 		action['domain'] = [('id', 'in', current_id)]
	# 	elif len(current_id) == 1:
	# 		action['views'] = [(self.env.ref('website_mega_menus.website_menu_form_view').id, 'form')]
	# 		action['res_id'] = current_id[0]
	# 	else:
	# 		action = {'type': 'ir.actions.act_window_close'}
	# 	return action

class Website(models.Model):
	_inherit = 'website'
	@api.model
	def get_public_categories(self, submenu=None):
		if(not submenu):
			submenus = self.env['website.menu'].sudo().search([])
			_logger.warning("submenus Website")
			for submenu in submenus:				
				_logger.warning(submenu)
				_logger.warning(submenu.name)
			submenu = self.env['website.menu'].sudo().browse(int(11))
			_logger.warning("submenu Website")
			_logger.warning(submenu)
		categs = []
		if submenu.categories_displayed == 'selected' and submenu.selected_categories:
			categs = submenu.selected_categories
		else:
			if submenu.root_category:
				categs = request.env['product.public.category'].sudo().search([('parent_id', '=', submenu.root_category.id)],order="sequence asc")
			else:
				categs = request.env['product.public.category'].sudo().search([('parent_id', '=', False)], order="sequence asc")
		return categs

	def create_fly_out_menu(self):
		mega_menu = self.env['website.menu'].search([('is_wk_mega_menu', '=', True),('website_id','=',request.website.id)])
		return mega_menu
