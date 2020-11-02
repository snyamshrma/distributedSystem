from flask import Blueprint, request, jsonify

peerInterfaceAPIs = Blueprint('peerInterfaceAPIs', __name__, template_folder='templates', static_folder='static', url_prefix='/peerInterface')

from middlewareService import handleRequest
from controller import peerInterfaceController

@peerInterfaceAPIs.route('/verifyChunk', methods=['POST'])
@handleRequest
def verifyChunk():
	"""
	This api verify claims sent by a peer to this peer for its authenticity.
	:return:
	"""
	claims = request.json
	return peerInterfaceController.verify(claims)