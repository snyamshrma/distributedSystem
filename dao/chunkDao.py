from db.models import Chunk, database

def insertChunk(payload, chunk, position):
	"""
	Adding chunk to the database.
	:param payload: payload object where payload string is being saved.
	:param chunk: chunks of the payload string.
	:param position: position at which chunk is located in the payload string.
	:return:
	"""
	chunkObject = Chunk()
	chunkObject.setPayload(payload)
	chunkObject.setChunk(chunk)
	chunkObject.setPosition(position)

	with database.atomic():
		chunkObject.save()

def fetchChunks(payloadObject):
	"""
	Fetches chunk from the using the payloadObject database.
	:param payloadObject: payload string object.
	:return:
	"""
	chunkObjects = Chunk.select().where(Chunk.payload == payloadObject).execute()
	return chunkObjects

def verifyChunk(chunk, position):
	"""
	Verify the chunk and its position in payload string.
	:param chunk: chunk of the payload string.
	:param position: position at which chunk is located in the payload string.
	:return:
	"""
	print(chunk, position)
	chunkObjects = Chunk.select().where((Chunk.chunk == chunk) & (Chunk.position == position)).execute()
	if len(chunkObjects) > 0:
		return True
	else:
		return False
