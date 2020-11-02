from db.models import Peer

def fetchPeers():
	peersObjects = Peer.select().execute()
	return peersObjects

def fetchPeersByType(type):
	if type is None or type.lower() == 'none':
		peersObjects = Peer.select().execute()
	else:
		peersObjects = Peer.select().where(Peer.type == type).execute()
	return peersObjects

def fetchByName(name):
	peersObjects = Peer.select().where(Peer.name == name).execute()
	return peersObjects
