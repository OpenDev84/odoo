$(document).ready(function () {
    $('.oe_website_sale').each(function () {
	var oe_website_sale = this;
	$(oe_website_sale).on('click', 'a.delete_order_line', function (ev) {
	    var $button = $(ev.currentTarget);
	    $input = $("input.js_quantity", $button.parent().parent());
	    $input.val(0);
	    $input.change();
	});
    
    });
});
