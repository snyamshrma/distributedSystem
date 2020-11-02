"""
	This file contains details of application server. Things like creating Flask application and running tornado server are done here.
"""
import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

import os
import argparse
from flask import Flask, request
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from db.models import database
from apis import adminInterfaceAPI, peerInterfaceAPI, logsAPI

# Initialize the Flask application
app = Flask(__name__, template_folder='templates', static_folder='static')

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='app')
	parser.add_argument('-p', '--port', help='name of the port on which application is to run.')

	logger.info('Creating Flask application context')
	app.config['RESTPLUS_JSON'] = {'indent': 5, 'separators': (',', ':')}
	app.secret_key = os.urandom(12)
	logger.info('Registering application APIs blueprints')

	app.register_blueprint(adminInterfaceAPI.adminInterfaceAPIs)
	app.register_blueprint(peerInterfaceAPI.peerInterfaceAPIs)
	app.register_blueprint(logsAPI.logsAPIs)

	app.debug = True

	#why CORS allowed?
	@app.after_request
	def setHeaders(response):
		response.headers["Access-Control-Allow-Origin"] = '*'
		# firefox does not take * as a wildcard in headers so need to explicitly specify the headers.
		response.headers["Access-Control-Allow-Headers"] = 'Content-Type, authorization'
		# response.headers["Access-Control-Allow-Headers"] = '*'
		response.headers["Access-Control-Allow-Methods"] = 'GET, POST, PUT, OPTIONS, DELETE'
		logger.debug('Completed Request for url {}'.format(request.url))
		return response


	@app.before_request
	def before_request():
		logger.info("Got the request for url {}. Sending it for processing.".format(request.url))
		database.connect()


	@app.teardown_request
	def _db_close(exc):  # don't remove the parameter - it is required
		if not database.is_closed():
			logger.debug('Close DB VIA api')
			database.close()

	args = vars(parser.parse_args())

	ipAddress = args["port"]
	portApp = int(ipAddress.split(':')[-1])
	# Wrapping Flask application in WSGI container of tornado
	logger.info('Creating WSGI wrapper around Flask application context')
	http_server_app = HTTPServer(WSGIContainer(app))
	http_server_app.bind(portApp)
	http_server_app.start(1)
	# Starting tornado server
	logger.info("Web application server started on port - {}".format(portApp))
	IOLoop.instance().start()
