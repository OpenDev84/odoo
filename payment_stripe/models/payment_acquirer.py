# -*- coding: utf-'8' "-*-"

from openerp.addons.payment.models.payment_acquirer import ValidationError
from openerp.osv import osv
from openerp.tools.float_utils import float_compare
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

import logging
import pprint

_logger = logging.getLogger(__name__)


class StripePaymentAcquirer(osv.Model):
    _inherit = 'payment.acquirer'

    def _get_providers(self, cr, uid, context=None):
        providers = super(StripePaymentAcquirer, self)._get_providers(cr, uid, context=context)
        providers.append(['stripe', 'Stripe Payment'])
        return providers

    def stripe_get_form_action_url(self, cr, uid, id, context=None):
        return '/web/stripe_payment'

    def create(self, cr, uid, values, context=None):
        """ Hook in create to create a default post_msg. This is done in create
        to have access to the name and other creation values. If no post_msg
        or a void post_msg is given at creation, generate a default one. """
        if values.get('provider') == 'stripe' and not values.get('post_msg'):
            values['post_msg'] = self._format_stripe_data(cr, uid, context=context)
        return super(StripePaymentAcquirer, self).create(cr, uid, values, context=context)

    def stripe_form_generate_values(self, cr, uid, id, partner_values, tx_values, context=None):
        base_url = self.pool['ir.config_parameter'].get_param(cr, SUPERUSER_ID, 'web.base.url')
        acquirer = self.browse(cr, uid, id, context=context)

        stripe_tx_values = dict(tx_values)
        stripe_tx_values.update({
            'email': partner_values['email'],
        })
        stripe_tx_values.update({
            'stripe_key': self.get_public_key(cr),
        })
        return partner_values, stripe_tx_values

    def get_public_key(self, cr):
	config = self.pool['ir.config_parameter']
	env = config.get_param(cr, SUPERUSER_ID, 'payment_stripe.environment')
	if env == 'test':
	    param = 'test_pk'
	else:
	    param = 'production_pk'
	full_param = 'payment_stripe.%s' % param
	return config.get_param(cr, SUPERUSER_ID, full_param)

class StripePaymentTransaction(osv.Model):
    _inherit = 'payment.transaction'

    def _stripe_form_get_tx_from_data(self, cr, uid, data, context=None):
        reference, amount, currency_name = data.get('reference'), data.get('amount'), data.get('currency_name')
        tx_ids = self.search(
            cr, uid, [
                ('reference', '=', reference),
            ], context=context)

        if not tx_ids or len(tx_ids) > 1:
            error_msg = 'received data for reference %s' % (pprint.pformat(reference))
            if not tx_ids:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.error(error_msg)
            raise ValidationError(error_msg)

        return self.browse(cr, uid, tx_ids[0], context=context)

    def _stripe_form_get_invalid_parameters(self, cr, uid, tx, data, context=None):
        invalid_parameters = []

        if float_compare(float(data.get('amount', '0.0')), tx.amount, 2) != 0:
            invalid_parameters.append(('amount', data.get('amount'), '%.2f' % tx.amount))
        if data.get('currency') != tx.currency_id.name:
            invalid_parameters.append(('currency', data.get('currency'), tx.currency_id.name))

        return invalid_parameters

    def _stripe_form_validate(self, cr, uid, tx, data, context=None):
        _logger.info('Validated stripe payment for tx %s: set as pending' % (tx.reference))
        return tx.write({'state': 'pending'})
