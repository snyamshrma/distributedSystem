import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

import json
import random
import hashlib
import requests
from string import ascii_letters

trustedServerIp = "http://localhost:1111"

def getRandomString(length=24, allowed_chars=ascii_letters):
	"""
	This function generate random string depending on the parameter passed for string and the allowed characters.
	:param length: the length for which the random string is to generated
	:param allowed_chars: character allowed in the random string.
	:return:
	"""
	return ''.join(random.choice(allowed_chars) for _ in range(length))

def encrypt(string, numberOfDigits = 8):
	"""
	This function encrypt the input string.
	:param string: string that has to encrypted
	:param numberOfDigits:
	:return:
	"""
	s = hashlib.shake_256()
	s.update(string)
	return s.hexdigest(numberOfDigits)

def addPayload(payload):
	"""
	This function adds payload to the trusted server
	:param payload: randomly generated string.
	:return:
	"""
	# adding payload to the trusted server.
	url = "{}/adminInterface/insert".format(trustedServerIp)
	data = {'payload': payload}
	logger.info("Adding payload to trusted server")
	response = requests.post(url, json=data)

	return response

def fetchPayload():
	"""
	This function fetches the payload from trusted server.
	:return:
	"""
	url = "{}/adminInterface/randomPayload".format(trustedServerIp)
	logger.info("Adding payload to trusted server")
	response = requests.get(url)

	return response

def claimExchange(randomPeer, payload):
	"""
	This function exchanges claims with the peer for verification.
	:param randomPeer: peer to which verification request is to be sent.
	:param payload: string fetched from the database whose chunks are to be verified.
	:return:
	"""
	# request claim exchanges.
	numberOfCharacterChunks = 4
	claims = []
	randomNumber = random.randint(1, numberOfCharacterChunks)
	position = 0
	for i in range(0, len(payload), numberOfCharacterChunks):
		chunk = payload[i:i + numberOfCharacterChunks]
		if position < randomNumber:
			claims.append({'chunk': chunk, 'position': position})
		position += 1
	url = "{}/peerInterface/verifyChunk".format(randomPeer)
	response = requests.post(url, json=claims)

	return claims, response

def getPeerList(peerType):
	"""
	This function fetches list of peers from the trusted server.
	:param peerType: type of peer in the database.
	:return:
	"""
	# request for list of peers.
	url = "{}/adminInterface/fetchPeers/{}".format(trustedServerIp, peerType)
	logger.info("Going to fetch list of peers for peer: {}".format(trustedServerIp))
	response = requests.get(url)

	return response

def saveLogs(peer, activity, data):
	"""
	This function sends request to trusted server to save logs.
	:param peer: peer whose logs are to be saved.
	:param activity: activity performed by the peer.
	:param data: data exchanged by the peer.
	:return:
	"""
	dataToSend = {'peer': peer, 'activity': activity, 'data': data}
	logger.info("Going to insert logs with data: {}".format(dataToSend))
	url = "{}/logs/insert".format(trustedServerIp)
	response = requests.post(url, json=dataToSend)

	return response


def fetchPeerActivity():
	url = "{}/logs/".format(trustedServerIp)
	response = requests.get(url, params={'peer': "http://localhost:1113"})

	return response
