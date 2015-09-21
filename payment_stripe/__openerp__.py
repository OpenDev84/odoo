{
    'name': 'Stripe Payment Acquirer',
    'category': 'Technical Settings',
    'summary': 'Payment Acquirer: Stripe Implementation',
    'version': '1.0',
    'description': """Stripe Payment Acquirer""",
    'author': 'OpenDev',
    'depends': ['payment'],
    'data': [
	'views/stripe.xml',
	'views/res_config.xml',
        'data/stripe.xml',
    ],
    'installable': True,
    'price':49.0,
    'currency':'EUR',
}
