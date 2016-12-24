import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class Default:
	PORT = 1031


class Development:
	DEBUG = True


class Production:
	pass


class Testing:
	TESTING = True


config = {
	'DEFAULT' : Default,
	'DEVELOPMENT': Development,
	'PRODUCTION': Production,
	'TESTING': Testing
}
