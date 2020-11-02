import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask import Blueprint, request

from middlewareService import handleRequest
from controller import logsController

logsAPIs = Blueprint('logsAPIs', __name__, template_folder='templates', static_folder='static', url_prefix='/logs')


@logsAPIs.route("/", methods=['GET'])
@handleRequest
def fetchRecords():
	"""
	This api fetches record depending on the type of activity performed by the peer.
	# :param peer: peer whose log records are being monitored.
	:return:
	"""
	print("hui")
	peer = request.args['peer']
	return logsController.processRecords(peer)

@logsAPIs.route("/insert", methods=['POST'])
@handleRequest
def insert():
	"""
	This api saves the log record.
	:return:
	"""
	dataToSave = request.json
	logsController.saveRecords(dataToSave)
	return

