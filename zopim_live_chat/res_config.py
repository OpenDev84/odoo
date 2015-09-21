# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models,fields

SUPPORTED_LANGS = [
    ('es', 'Spanish'),
    ('en', 'English'),
    ('af', 'Afrikaans'),
    ('sq', 'Albanian'),
    ('ar', 'Arabic'),
    ('az', 'Azerbaijani'),
    ('eu', 'Basque'),
    ('bg', 'Bulgarian'),
    ('ca', 'Catalan'),
    ('zh_CN', 'Chinese (China)'),
    ('zh_TW', 'Chinese (Taiwan)'),
    ('hr', 'Croatian'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('nl', 'Dutch'),
    ('et', 'Estonian'),
    ('fo', 'Faroese'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('gl', 'Galician'),
    ('ka', 'Georgian'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('he', 'Hebrew'),
    ('hu','Hungarian'),
    ('is', 'Icelandic'),
    ('id', 'Indonesian'),
    ('ga', 'Irish'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('ku', 'Kurdish'),
    ('lv', 'Latvian'),
    ('lt', 'Lithuanian'),
    ('mk', 'Macedonian'),
    ('ms', 'Malay'),
    ('mn', 'Mongolian'),
    ('nb', 'Norwegian Bokmal'),
    ('fa', 'Persian'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('pt_BR', 'Portuguese Brazil'),
    ('ro', 'Romanian'),
    ('ru', 'Russian'),
    ('sr', 'Serbian'),
    ('si', 'Sinhala'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('th', 'Thai'),
    ('tr', 'Turkish'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('vi', 'Vietnamese'),
]
class ZopimConfiguration(models.TransientModel):
    _name = 'zopim.config.settings'
    _inherit = 'res.config.settings'

    key = fields.Char('Zopim Live Chat Key', required=True)
    color_primary = fields.Char('Primary Color', required=False)
    color_badge = fields.Char('Badge Color', required=False)
    lang = fields.Selection(SUPPORTED_LANGS, string='Language')
    online_greetings = fields.Char('Online')
    offline_greetings = fields.Char('Offline')
    theme = fields.Selection([('simple', 'Simple'), ('classic', 'Classic')], 'Theme')
    layout = fields.Selection([('image_right', 'Image on right, text on left'), 
				('image_left', 'Image on left, text on right'), 
				('image_only', 'Image only'),
				('text_only', 'Text only')
			      ], 'Layout')
    
    def get_default_theme(self, cr, uid, ids, context=None):
        theme = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.theme", default='classic', context=context)
        return {'theme': theme or False}
        
    def set_theme(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.theme", record.theme or False, context=context)
	    
    def get_default_layout(self, cr, uid, ids, context=None):
        layout = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.layout", default='image_left', context=context)
        return {'layout': layout or False}
        
    def set_layout(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.layout", record.layout or False, context=context)
	    
    def get_default_online_greetings(self, cr, uid, ids, context=None):
        online_greetings = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.online_greetings", default='Chat with us', context=context)
        return {'online_greetings': online_greetings or False}
        
    def set_online_greetings(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.online_greetings", record.online_greetings or False, context=context)
	    
    def get_default_offline_greetings(self, cr, uid, ids, context=None):
        offline_greetings = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.offline_greetings", default='Leave us a message', context=context)
        return {'offline_greetings': offline_greetings or False}
        
    def set_offline_greetings(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.offline_greetings", record.offline_greetings or False, context=context)

    def get_default_lang(self, cr, uid, ids, context=None):
        lang = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.lang", default='en', context=context)
        return {'lang': lang or False}
        
    def set_lang(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.lang", record.lang or False, context=context)


    def get_default_key(self, cr, uid, ids, context=None):
        key = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.key", default=None, context=context)
        return {'key': key or False}
        
    def set_key(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.key", record.key or False, context=context)

    def get_default_color_primary(self, cr, uid, ids, context=None):
        color_primary = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.color_primary", default=None, context=context)
        return {'color_primary': color_primary or False}
        
    def set_color_primary(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.color_primary", record.color_primary or False, context=context)

    def get_default_color_badge(self, cr, uid, ids, context=None):
        color_badge = self.pool.get("ir.config_parameter").get_param(cr, uid, "zopim_live_chat.color_badge", default=None, context=context)
        return {'color_badge': color_badge or False}
        
    def set_color_badge(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "zopim_live_chat.color_badge", record.color_badge or False, context=context)

