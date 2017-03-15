# -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate

#Get the logger
_logger = logging.getLogger(__name__)


class purchase_order(models.Model):
	_inherit = 'purchase.order'

	#@api.one
	#def _compute_price_unit(self):
	#	if self.product_qty > 0:
	#		self.price_unit = self.price_subtotal / self.product_qty

	#@api.onchange('discount')
	#def onchange_po_discount(self):
	#	if self.discount > 0 and self.discount < 100:
	#		for line in self.order_line:
	#

	@api.depends('order_line.price_total','discount')
	def _amount_all(self):
		for order in self:
			amount_untaxed = amount_tax = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
		                # FORWARDPORT UP TO 10.0
                		if order.company_id.tax_calculation_rounding_method == 'round_globally':
		                    taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
                		    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
		                else:
                		    amount_tax += line.price_tax
			if order.discount > 0 and order.discount < 100:
				order_discount = 1 - (order.discount / 100)
				comp_order_discount = 1 - order_discount
			else:
				order_discount = 1
			comp_order_discount = 1 - order_discount
			order.update({
                		'amount_untaxed': order.currency_id.round(amount_untaxed * order_discount),
		                'amount_tax': order.currency_id.round(amount_tax * order_discount),
                		'amount_total': amount_untaxed * order_discount + amount_tax * order_discount,
				'amount_discount': (amount_untaxed * comp_order_discount + amount_tax * comp_order_discount) * (-1),
		        })

	@api.one
	@api.constrains('discount')
	def _check_discount(self):
		if self.discount < 0 or self.discount > 99.99:
			raise ValidationError("Descuento debe ser mayor a 0 y menor a 100")

	discount = fields.Float('Descuento')
	amount_discount = fields.Monetary('Monto Descuento', store=True, readonly=True, compute='_amount_all')

