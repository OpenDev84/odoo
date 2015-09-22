{
    'name': "Session Lockscreen",
    'version': '0.1',
	'author': 'OpenDev',
	'sequence': 3,
	'summary': 'Lock the user session with a PIN code',
    'description': """
    """,
    'category': 'Tools',
    'depends': ['web'],
    'data': ['lockscreen.xml', 'res_users_view.xml'],
    'qweb': [
		'static/src/xml/lockscreen.xml',
		'static/src/xml/base.xml',
    ],
    'price':15.0,
    'currency':'EUR',
}
