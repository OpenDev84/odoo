# -*- coding: utf-8 -*-
import stripe

import logging
import pprint
import werkzeug
import urlparse
import requests
import simplejson

from openerp import http, SUPERUSER_ID
from openerp.addons.web import http
from openerp.http import request

_logger = logging.getLogger(__name__)
    
class StripePayment(http.Controller):
	
    def get_secret_key(self, cr):
	config = request.registry['ir.config_parameter']
	env = config.get_param(request.cr, SUPERUSER_ID, 'payment_stripe.environment')
	if env == 'test':
	    param = 'test_sk'
	else:
	    param = 'production_sk'
	full_param = 'payment_stripe.%s' % param
	return config.get_param(request.cr, SUPERUSER_ID, full_param)
	
    @http.route('/web/stripe_payment', type='http', auth="public")
    def stripe_payment(self, **post):
	cr, uid, context = request.cr, SUPERUSER_ID, request.context
		
	stripe.api_key = self.get_secret_key(cr)
	# Get the credit card details submitted by the form
	if not 'token' in post:
	    return 
			
	token = post['token']
	amount = float(post['amount'])
	currency = post['currency']
		
	hostname = urlparse.urlparse(request.httprequest.base_url).hostname.upper(),
	# Create the charge on Stripe's servers - this will charge the user's card
	try:
	    charge = stripe.Charge.create(
		amount=int(amount)*100, # amount in cents, again
		currency=currency,
		source=token,
		description=hostname[0],
		statement_descriptor=hostname[0],
		capture=False
		)
	except stripe.error.CardError, e:
	    # The card has been declined
	    print e
			
	_logger.info('Beginning form_feedback with post data %s', pprint.pformat(post))  # debug
	request.registry['payment.transaction'].form_feedback(cr, uid, post, 'stripe', context)
	return werkzeug.utils.redirect(post.pop('return_url', '/'))
