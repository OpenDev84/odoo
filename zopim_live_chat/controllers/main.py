import werkzeug.utils

from openerp import http
from openerp import SUPERUSER_ID
from openerp.addons.web.controllers.main import Home
from openerp.addons.web.controllers.main import ensure_db
from openerp.addons.web.controllers.main import login_redirect
from openerp.http import request

class MyHome(Home):
    
    def get_zopim_key(self):
        config = request.registry['ir.config_parameter']
        key = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.key')
        return key
	
    def get_zopim_color_primary(self):
        config = request.registry['ir.config_parameter']
        color_primary = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.color_primary')
        return color_primary
	
    def get_zopim_color_badge(self):
        config = request.registry['ir.config_parameter']
        color_badge = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.color_badge')
        return color_badge
	
    def get_zopim_lang(self):
        config = request.registry['ir.config_parameter']
        lang = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.lang')
        return lang
	
    def get_zopim_online_greetings(self):
        config = request.registry['ir.config_parameter']
        online = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.online_greetings')
        return online
    
    def get_zopim_offline_greetings(self):
        config = request.registry['ir.config_parameter']
        offline = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.offline_greetings')
        return offline
	
    def get_zopim_theme(self):
        config = request.registry['ir.config_parameter']
        theme = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.theme')
        return theme
    
    def get_zopim_layout(self):
        config = request.registry['ir.config_parameter']
        layout = config.get_param(request.cr, SUPERUSER_ID, 'zopim_live_chat.layout')
        return layout
	
    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        ensure_db()
        if request.session.uid:
            if kw.get('redirect'):
                return werkzeug.utils.redirect(kw.get('redirect'), 303)
            if not request.uid:
                request.uid = request.session.uid

            menu_data = request.registry['ir.ui.menu'].load_menus(request.cr, request.uid, context=request.context)
	    key = self.get_zopim_key()
	    badge = self.get_zopim_color_badge()
	    primary = self.get_zopim_color_primary()
	    lang = self.get_zopim_lang()
	    online = self.get_zopim_online_greetings()
	    offline = self.get_zopim_offline_greetings()
	    theme = self.get_zopim_theme()
	    layout = self.get_zopim_layout()
	    
	    user = request.registry['res.users'].browse(request.cr, request.uid, request.uid, context=request.context)
	    
            return request.render('web.webclient_bootstrap', qcontext={'menu_data': menu_data, 
								       'key': key, 
								       'badge': badge, 
								       'primary': primary, 
								       'username': user.name, 
								       'email': user.email, 
								       'lang': lang, 
								       'online': online, 
								       'offline': offline, 
								       'theme': theme,
								       'layout': layout})
        else:
            return login_redirect()

    
