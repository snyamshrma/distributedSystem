import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

import json
import requests

trustedServerIp = "http://localhost:1111"

def verify(claims):
	"""
	This function sends the request to trusted api server to check the authenticity of the claims exchanged.
	:param claims:
	:return:
	"""
	url = "{}/adminInterface/verifyChunk".format(trustedServerIp)
	logger.info("Fetching list of peers for getting the peers responsible for traffic situation currently.")
	response = requests.post(url, json=claims)

	decodedResponse = json.loads(response.content.decode("utf-8"))['data']
	return decodedResponse