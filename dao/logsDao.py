from db.models import Logs, database

def getLogs(peerObject):
	"""
	Fetches log records based on peer.
	:param peerObject: peer whose log records are being monitored.
	:return:
	"""
	logsObject = Logs.select().where(Logs.peer == peerObject).execute()
	return logsObject

def insert(peer, activity, data):
	"""
	Add activity performed and the data shared  by the peer to the database.
	:param peer:
	:param activity:
	:param data:
	:return:
	"""
	logObject = Logs()
	logObject.setData(data)
	logObject.setActivity(activity)
	logObject.setPeer(peer)
	with database.atomic():
		logObject.save()

	return logObject