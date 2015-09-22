import random

from openerp import models, api, fields

def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)
    
class res_users(models.Model):
    _inherit = 'res.users'
    
    @api.model
    def _get_default_pin(self):
	return randomDigits(4)

    pin = fields.Integer('PIN Code', required=True, default=_get_default_pin)
