$(document).ready(function () {
	var amount = $('#amount', $('#stripe_button').parent()).val() * 100;
	var currency = $('#currency', $('#stripe_button').parent()).val();
	var reference = $('#reference', $('#stripe_button').parent()).val();
	var company = $('#company', $('#stripe_button').parent()).val();
	var return_url = $('#return_url', $('#stripe_button').parent()).val();
	var stripe_key = $('#stripe_key', $('#stripe_button').parent()).val();
	
	var handler = StripeCheckout.configure({
		key: stripe_key,
		image: '/payment_stripe/static/src/img/ico.png',
		token: function(token) {
			// Use the token to create the charge with a server-side script.
			// You can access the token ID with `token.id`
			//$.post( "/web/stripe_payment",{token: token.id, amount: amount, currency: currency, reference: reference, return_url: return_url});
			$("form[id='payment-form']").prepend('<input type="hidden" id="token" name="token" />');
			$("input[id='token']").val(token.id);
			$("form[id='payment-form']").submit();
		}
	});
	
	$('#stripe_button').on('click', function(e) {
		// Open Checkout with further options
		handler.open({
		name: company,
		description: 'Pay with Credit Card',
		amount: amount,
		email:$('#email', $('#stripe_button').parent()).val(),
		currency: currency
		});
		e.preventDefault();
	});

	// Close Checkout on page navigation
	$(window).on('popstate', function() {
		handler.close();
	});
		
});
