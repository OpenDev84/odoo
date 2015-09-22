
openerp.session_lockscreen = function (instance) {
    instance.web.client_actions.add('session.lock', 'instance.session_lockscreen.Action');
    instance.session_lockscreen.Action = instance.web.Widget.extend({
        template: 'Lock',
        login: null,
        password: null,
        pin: null,
        db: null,
        
        events: {
			'click .pin_code_board button': 'add_pin_input',
			keyup: 'onKeyup',
			'click .unlock_button': 'unlock_session'
		},
        init: function () {
            this._super.apply(this, arguments);
            var self = this;
            var func = new instance.web.Model("res.users").get_func("read");
            this.alive(func(self.session.uid, ["login", "password", "pin"])).then(function(res){
					self.login = res.login;
					self.password = res.password;
					self.pin = res.pin;
					self.db = instance.session.db;
					var $avatar = self.$el.find('.oe_lockscreen_avatar');
					$avatar.attr('src', $avatar.data('default-src'));
					var avatar_src = self.session.url('/web/binary/image', {model:'res.users', field: 'image_small', id: self.session.uid});
					$avatar.attr('src', avatar_src);
			}).then(function(res){
				self.hide_bars();
				self.remove_credentials();
			});
        },
        
        hide_bars: function(){
		    instance.webclient.toggle_bars(false);
		    //instance.webclient('tr:has(td.navbar),.oe_leftbar').toggle(false);
		    $('.navbar').hide();
		},
		
	show_bars: function(){
		    instance.webclient.toggle_bars(true);
		    $('.navbar').show();
		},
		
	remove_credentials: function(){
            this.session.session_logout().done(function () {
                $(window).unbind('hashchange', self.on_hashchange);
            });
		},
        
        add_pin_input: function(button){
        	this.$('.pin_value_input').focus();
			var value = this.$('.pin_value_input').val();
			var pin_input = $(button.currentTarget).val();
			if (pin_input === "clear"){
				if (value.length == 1 ) {
					this.change_button_status(0,0);
				}
				if (value.length == 4 ) {
					this.change_button_status(0,1);
				}
				this.$('.pin_value_input').val(value.substring(0,value.length-1));
			}else{
				if (value.length == 0 ) {
					this.change_button_status(1,0);
				}
				if (value.length < 4 ) {
					this.$('.pin_value_input').val(value+pin_input);
				}
				if (value.length == 3 ) {
					this.change_button_status(1,1);
				}
			}
		},
		
		/**
		 * Change the Clear/Unlock button images
		 * 
		 * @param state = 0 disable
		 * 				= 1 enable
		 * 
		 * @param button the button to change
		 *        0 = clear
		 *        1 = submit          
		 * */
		change_button_status: function(state,button){
			switch (button){
				case 0:
					if (state===1) {
						this.$('.clear_button img').attr('src','/session_lockscreen/static/src/img/clear-a.png');
					}else{
						this.$('.clear_button img').attr('src','/session_lockscreen/static/src/img/clear.png');
					}					
					break;
				case 1:
					if (state===1) {
						this.$('.unlock_button img').attr('src','/session_lockscreen/static/src/img/unlock-a.png');
					}else{
						this.$('.unlock_button img').attr('src','/session_lockscreen/static/src/img/unlock.png');
					}
					break;
			}
		},
		
		onKeyup: function (e) {
			var value = this.$('.pin_value_input').val();
			if(e.which!=$.ui.keyCode.BACKSPACE){
				if (value.length >= 4 ) {
					switch (e.which) {
						case $.ui.keyCode.ENTER:
							this.unlock_session();
							break;
						default:
							this.$('.pin_value_input').val(value.substring(0,4));
							break;							
					}
				}
				if (value.length == 1 ) {
					this.change_button_status(1,0);
				}
				if (value.length == 4 ) {
					this.change_button_status(1,1);
				}
			}else{
				if (value.length == 0 ) {
					this.change_button_status(0,0);
				}
				if (value.length == 3 ) {
					this.change_button_status(0,1);
				}
			}
		},
		
		unlock_session: function(){
			var value = this.$('.pin_value_input').val();
			if (value.length == 4 ) {
				if (value == this.pin){
					this.$(".oe_login_error_message").removeClass('alert');
					this.$(".oe_login_error_message").removeClass('alert-danger');
					this.$(".oe_login_error_message").text("");
					var self = this;
					this.rpc("/web/session/authenticate", {db:this.db,login:this.login,password:this.password}).then(function(){
						self.$el.addClass("oe_hidden");
						self.show_bars();
						instance.web.redirect(_url, false);
					});
					
					
				}
				else{
					this.$(".oe_login_error_message").addClass("alert");
					this.$(".oe_login_error_message").addClass("alert-danger");
					this.$(".oe_login_error_message").text("Incorrect PIN Code");
				}
			}
		},
    });
    
	instance.web.UserMenu =  instance.web.UserMenu.extend({
		on_menu_lock: function() {
			var self = this;
			_url = window.location.href;
			if (!this.getParent().has_uncommitted_changes()) {
				self.rpc("/web/action/load", { action_id: "session_lockscreen.action_session_lock" }).done(function(result) {
					result.res_id = instance.session.uid;
					self.getParent().action_manager.do_action(result);
				});
			}
		},
	});
};
