import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

from flask import Blueprint, request

from middlewareService import handleRequest
from controller import adminInterfaceController

adminInterfaceAPIs = Blueprint('adminInterfaceAPIs', __name__, template_folder='templates', static_folder='static', url_prefix='/adminInterface')

@adminInterfaceAPIs.route('/insert', methods=['POST'])
@handleRequest
def addPayload():
	"""
	This api insert the payload to the database.
	:return:
	"""
	payload = request.json['payload']
	return adminInterfaceController.insertPayload(payload)

@adminInterfaceAPIs.route('/fetchPeers/<type>', methods=['GET'])
@handleRequest
def fetchPeers(type):
	"""
	This api fetches peers by there type like server or peer.
	:param type: type of peer existing in the database.
	:return:
	"""
	return adminInterfaceController.fetchPeers(type)

@adminInterfaceAPIs.route('/fetchPayload/<payloadId>', methods=['GET'])
@handleRequest
def fetchPayload(payloadId):
	"""
	This api fetches payload using the given payloadId provided by the peer.
	:param payloadId: randomly generated alphanumeric string.
	:return:
	"""
	return adminInterfaceController.fetchPayload(payloadId)

@adminInterfaceAPIs.route('/randomPayload', methods=['GET'])
@handleRequest
def randomPayload():
	"""
	This api fetches random payload from the database.
	:return:
	"""
	return adminInterfaceController.fetchRandomPayload()

@adminInterfaceAPIs.route('/verifyChunk', methods=['POST'])
@handleRequest
def verifyChunk():
	"""
	This api verify the chunks send by the peer for claim exchange.
	:return:
	"""
	claims = request.json
	return adminInterfaceController.verifyChunk(claims)
