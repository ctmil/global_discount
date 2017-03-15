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

	discount = fields.Float('Descuento')


