import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

import json
import time
import random

import utils
from constants import PeerType, Activity


def simulate():
	count = 1
	while True:
		startTime = time.time()
		# creating a random generated payload.
		payload = utils.getRandomString(length=random.randint(10, 16))

		# adding payload to the trusted server.
		payloadId = utils.addPayload(payload)
		payloadIdDecoded = json.loads(payloadId.content.decode("utf-8"))['data']
		logger.info("payloadId for payload {} is {}".format(payload, payloadIdDecoded))

		# fetching a random peer which is responsible for traffic.
		peerObjects = utils.getPeerList(PeerType.PEER)
		random.shuffle(peerObjects)
		randomPeer = peerObjects[0]
		logger.info("Got peer {} responsible for traffic.".format(randomPeer))

		# starting claim verification part.
		if count % 5 == 0:
			# randomly generating a payload to present bad claims from it.
			payload = utils.getRandomString(length=random.randint(10, 16))
		else:
			# fetching payload from the trusted server to present correct claims.
			payloadDict = utils.fetchPayload()
			payload = json.loads(payloadDict.content.decode("utf-8"))['data']

		# verifying claims using another peer from trusted server.
		verifyingClaimPeer = list(set(peerObjects) - set(randomPeer))
		random.shuffle(verifyingClaimPeer)
		randomVerifyingClaimPeer = verifyingClaimPeer[0]
		claims, claimResponse = utils.claimExchange(randomVerifyingClaimPeer, payload)
		claimResponseDecoded = json.loads(claimResponse.content.decode("utf-8"))['data']
		logger.info("Claims: {} and the responses by another peer: {}".format(claims, claimResponseDecoded))
		utils.saveLogs(randomPeer, Activity.CLAIMS_EXCHANGED, claims)
		utils.saveLogs(randomVerifyingClaimPeer, Activity.CLAIMS_RESPONSE, claimResponseDecoded)

		# checking list of all peers from trusted server.
		logger.info("Peer: {} checking list of all peers.".format(randomPeer))
		peerList = utils.getPeerList(PeerType.PEER)
		peerListDecoded = json.loads(peerList.content.decode("utf-8"))['data']
		logger.info("List of peers: {}".format(peerListDecoded))
		utils.saveLogs(randomPeer, Activity.COMMS_WITH_TRUSTED_SERVER, peerListDecoded)

		# to simulate real time behaviour sleeping for an interval between 10 - 20 seconds.
		sleepTime = random.randint(10, 20)
		logger.info("Sleeping for {} seconds.".format(sleepTime))
		time.sleep(sleepTime)

		count += 1

		# stopping the simulation if it is running for more than 5 minutes.
		diff = time.time() - startTime
		if diff > 5*60:
			logger.info("Stopping the simulation after 5 minutes have passed.")
			break


if __name__ == '__main__':
	simulate()