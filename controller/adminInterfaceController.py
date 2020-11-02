import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
import random

import utils
from dao import peerDao, payloadDao, chunkDao

def insertPayload(payload, numberOfCharacterChunks = 4):
	"""
	Inserting payload to database with a randomly generated payloadId.
	:param payload: String that has to be saved in the database.
	:param numberOfCharacterChunks: Number of characters for which chunks are created.
	:return:
	"""
	while True:
		# looping to get a unique payloadId
		payloadId = utils.getRandomString(12)
		if payloadDao.checkExist(payloadId):
			logger.info("PayloadId {} already exist. Trying to find unique id.".format(payloadId))
		else:
			logger.info("Found unique payloadId: {}".format(payloadId))
			break

	payloadObject = payloadDao.insertPayload(payloadId, payload)

	# inserting chunks to database.
	position = 0
	for i in range(0, len(payload), numberOfCharacterChunks):
		chunk = payload[i:i+numberOfCharacterChunks]
		# insert chunks to database.
		chunkDao.insertChunk(payloadObject, chunk, position)
		position += 1

	return payloadId

def fetchPeers(type):
	"""
	Fetching the list of peers from database depending on there type.
	:return:
	"""
	peersObjects = peerDao.fetchPeersByType(type)
	return [p.name for p in peersObjects]

def fetchPayload(payloadId):
	"""
	Fetching payload and its chunks and encrypting it.
	:param payloadId: randomly generated alphanumeric string.
	:return:
	"""
	chunks = []
	payloadObject = payloadDao.fetchPayload(payloadId)
	chunkObjects = chunkDao.fetchChunks(payloadObject)
	for chunkObject in chunkObjects:
		# encrypt the chunks
		chunk = chunkObject.getChunk()
		hashChunk = utils.encrypt(chunk)
		chunks.append(hashChunk)

	rootChunk = ''.join(i for i in chunks)
	# encrypt the rootChunk
	rootHash = utils.encrypt(rootChunk)
	dataToReturn = {'chunks': chunks, 'rootHash': rootHash, 'claimedString': payloadObject.getPayload()}

	return dataToReturn

def fetchRandomPayload():
	"""
	Fetching a random payload.
	:return:
	"""
	payloadObjects = payloadDao.fetchRandomPayload()
	payloadObjects = [p.getPayload() for p in payloadObjects]
	random.shuffle(payloadObjects)

	return payloadObjects[0]

def verifyChunk(claims):
	"""
	Verifying whether the claims given by the peer is correct or not.
	:param claims: list of chunks and their position in the payload.
	:return:
	"""
	results = []
	for claim in claims:
		chunk = claim['chunk']
		position = claim['position']
		results.append(chunkDao.verifyChunk(chunk, position))

	return results