from db.models import Payload, database

def fetchPayload(payloadId):
	payloadObjects = Payload.select().where(Payload.payloadId == payloadId).execute()
	return payloadObjects

def fetchRandomPayload():
	payloadObjects = Payload.select().execute()
	return payloadObjects

def insertPayload(payloadId, payload):
	payloadObject = Payload()

	payloadObject.setPayload(payload)
	payloadObject.setPayloadId(payloadId)

	with database.atomic():
		payloadObject.save()

	return payloadObject

def checkExist(payloadId):
	payloadObjects = fetchPayload(payloadId)
	if len(payloadObjects) > 0:
		return True
	else:
		return False
