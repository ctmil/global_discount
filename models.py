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

	@api.onchange('discount')
	def onchange_po_discount(self):
		if self.discount > 0 and self.discount < 100:
			for line in self.order_line:
				line.write({'discount': self.discount})

	@api.one
	@api.constrains('discount')
	def _check_discount(self):
		if self.discount < 0 or self.discount > 99.99:
			raise ValidationError("Descuento debe ser mayor a 0 y menor a 100")

	discount = fields.Float('Descuento')


