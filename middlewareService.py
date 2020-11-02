from functools import wraps
from flask import jsonify

import response, constants

import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

def handleRequest(f):
	@wraps(f)
	def handler(*args, **kwargs):
		try:
			data = f(*args, **kwargs)
			responseData = jsonify(response.setResponseData(constants.StatusCodes.SUCCESS, message="Data fetched",
															jsonData=data))
		except Exception as e:
			logger.exception("Exception occurred: {}".format(e))
			responseData = jsonify(response.setResponseData(constants.StatusCodes.INTERNAL_SERVER_ERROR, errorMessage=str(e)))

		return responseData

	return handler