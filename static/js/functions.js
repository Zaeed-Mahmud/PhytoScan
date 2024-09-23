
;(function($){
	function AjaxPopup(options){
		this.options = $.extend({
			holder: null,
			button: '.btn-more',
			holderBox: 'body',
			ajaxHold: '#ajax-holder',
			appendToBody: false,
			attr: 'href',
			animSpeed: 500
		}, options);

		this.init();
	}
	AjaxPopup.prototype = {
		init: function(){
			this.findElements();
			this.makeCallback('onInit', this);
			this.attachEvents();
		},
		findElements: function(){
			this.holder = jQuery(this.options.holder);
			this.button = this.holder.find(this.options.button);
			this.ajaxHold = this.holder.find(this.options.ajaxHold);

		},
		attachEvents: function(){
			var self = this;
			this.clickHandler = function(e){
				e.preventDefault();
				var attr = self.button.attr(self.options.attr);
				if(attr != '#'){
					e.preventDefault();
					self.ajaxLoad(attr).done(function(data){
						var content = jQuery(data).filter('.blogs-block').css({opacity: 0});
						var btnAjax = jQuery(data).filter('.btn-load');

						if(self.options.appendToBody) content.appendTo(jQuery(self.options.holderBox));
						else content.appendTo(self.ajaxHold);

						if(btnAjax.length) self.button.attr('href', btnAjax.attr('href')); 
						else self.button.hide();
					
						content.stop().animate({opacity: 1}, self.options.animSpeed);
						self.makeCallback('onChange', self);
					});
				}
			};
			this.button.on('click', this.clickHandler);
		},
		ajaxLoad: function(url){
			var d = jQuery.Deferred();
			jQuery.ajax({
				url: url,
				type: 'get',
				cache: false,
				dataType: "html",
				success: function(data){
					d.resolve(data);
				},
				error: function(jqXHR, textStatus, errorThrown){
					d.reject(jqXHR, textStatus, errorThrown);
				}
			});
			return d;
		},
		makeCallback: function(name) {
			if(typeof this.options[name] === 'function') {
				var args = Array.prototype.slice.call(arguments);
					args.shift();
					this.options[name].apply(this, args);
				}
			}
		};

	$.fn.ajaxPopup = function(options){
		return this.each(function(){
			$(this).data('AjaxPopup', new AjaxPopup($.extend(options, {holder:this})));
		});
	};
})(jQuery);