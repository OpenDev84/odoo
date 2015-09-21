from openerp import models, fields

class StripeConfigWizard(models.TransientModel):
    _name = 'payment_stripe.config.settings'
    _inherit = 'res.config.settings'

    environment = fields.Selection([('test', 'Test'), ('production', 'Production')], 'Environment')
    test_sk = fields.Char('Test secret key')
    test_pk = fields.Char('Test public key')
    production_sk = fields.Char('Production secret key')
    production_pk = fields.Char('Production public key')
    
    def get_default_environment(self, cr, uid, ids, context=None):
        environment = self.pool.get("ir.config_parameter").get_param(cr, uid, "payment_stripe.environment", default='test', context=context)
        return {'environment': environment or False}

    def set_environment(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "payment_stripe.environment", record.environment or '', context=context)
            
    def get_default_test_sk(self, cr, uid, ids, context=None):
        test_sk = self.pool.get("ir.config_parameter").get_param(cr, uid, "payment_stripe.test_sk", default=None, context=context)
        return {'test_sk': test_sk or False}

    def set_test_sk(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "payment_stripe.test_sk", record.test_sk or '', context=context)
            
    def get_default_test_pk(self, cr, uid, ids, context=None):
        test_pk = self.pool.get("ir.config_parameter").get_param(cr, uid, "payment_stripe.test_pk", default=None, context=context)
        return {'test_pk': test_pk or False}

    def set_test_pk(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "payment_stripe.test_pk", record.test_pk or '', context=context)

    def get_default_production_sk(self, cr, uid, ids, context=None):
        production_sk = self.pool.get("ir.config_parameter").get_param(cr, uid, "payment_stripe.production_sk", default=None, context=context)
        return {'production_sk': production_sk or False}

    def set_production_sk(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "payment_stripe.production_sk", record.production_sk or '', context=context)
            
    def get_default_production_pk(self, cr, uid, ids, context=None):
        production_pk = self.pool.get("ir.config_parameter").get_param(cr, uid, "payment_stripe.production_pk", default=None, context=context)
        return {'production_pk': production_pk or False}

    def set_production_pk(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "payment_stripe.production_pk", record.production_pk or '', context=context)
