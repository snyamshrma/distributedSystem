import logging
logging.basicConfig(format='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s] - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
from dao import logsDao, peerDao

def processRecords(peerName):
	"""
	Fetches log record of the peer and processes it to be in readable format.
	:param peerName: name of the peer whose log records are being monitored.
	:return:
	"""
	peerObject = peerDao.fetchByName(peerName)
	peerObject = [p for p in peerObject][0]
	logsObjects = logsDao.getLogs(peerObject)

	dataToReturn = {}
	for logsObject in logsObjects:
		activity = logsObject.getActivity()
		data = logsObject.getData()
		if activity not in dataToReturn:
			dataToReturn[activity] = []
		dataToReturn[activity].append(data)

	return dataToReturn

def saveRecords(dataToSave):
	"""
	Saving the logs(activity) performed by the peer.
	:param dataToSave:
	:return:
	"""
	peerObject = peerDao.fetchByName(dataToSave['peer'])
	peerObject = [p for p in peerObject][0]
	logsDao.insert(peerObject, dataToSave['activity'], dataToSave['data'])
	logger.info("Successfully saved logs of peer: {} for activity: {}".format(dataToSave['peer'], dataToSave['activity']))