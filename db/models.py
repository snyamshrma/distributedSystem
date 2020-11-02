import time
import json
from peewee import Model, CharField, BigIntegerField, PrimaryKeyField, ForeignKeyField, IntegerField
from peewee import MySQLDatabase

database = MySQLDatabase(None)

database.init('distributedSystem', user='root',password='a', host='localhost')

class BaseModel(Model):
	"""
		Base model which is extended by most of the other classes.
		It contains fields which are common across classes.
	"""
	id = PrimaryKeyField()
	created = BigIntegerField()
	updated = BigIntegerField()
	deleted = BigIntegerField(null=True)

	def __init__(self, **kwargs):
		Model.__init__(self, **kwargs)
		#adding if conditions to only init time when it is none i.e. when a fresh model is created, this caused and issue using peewee version 3.5.2 and above
		if self.created is None:
			self.created = int(time.time())
		if self.updated is None:
			self.updated = int(time.time())

	def getId(self):
		return self.id

	def getCreated(self):
		return self.created

	def getUpdated(self):
		return self.updated

	def getDeleted(self):
		return self.deleted

	def setId(self, val):
		self.id = val

	def setCreated(self, val):
		self.created = val

	def setUpdated(self, val):
		self.updated = val

	def setDeleted(self, val):
		self.deleted = val

	class Meta:
		database = database

class Peer(BaseModel):
	name = CharField(null=False)
	type = CharField(null=False)

	def __init__(self, **kwargs):
		BaseModel.__init__(self, **kwargs)

	def getName(self):
		return self.name

	def setName(self, val):
		self.name = val

	def getType(self):
		return self.type

	def setType(self, val):
		self.type = val

class Payload(BaseModel):
	payload = CharField(null=False)
	payloadId = CharField(null=False)

	def __init__(self, **kwargs):
		BaseModel.__init__(self, **kwargs)

	def getPayload(self):
		return self.payload

	def setPayload(self, val):
		self.payload = val

	def getPayloadId(self):
		return self.payloadId

	def setPayloadId(self, val):
		self.payloadId = val


class Chunk(BaseModel):
	chunk = CharField(null=False)
	position = IntegerField(null=False, default=1)
	payload = ForeignKeyField(Payload, related_name="chunks")

	def __init__(self, **kwargs):
		BaseModel.__init__(self, **kwargs)

	def getChunk(self):
		return self.chunk

	def setChunk(self, val):
		self.chunk = val

	def getPayload(self):
		return self.payload

	def setPayload(self, val):
		self.payload = val

	def getPosition(self):
		return self.position

	def setPosition(self, val):
		self.position = val

class Logs(BaseModel):
	activity = CharField(null=False)
	data = CharField(null=True)
	peer = ForeignKeyField(Peer, related_name="logs")

	def __init__(self, **kwargs):
		BaseModel.__init__(self, **kwargs)

	def getActivity(self):
		return self.activity

	def setActivity(self, val):
		self.activity = val

	def getData(self):
		return json.loads(self.data)

	def setData(self, val):
		self.data = json.dumps(val)

	def getPeer(self):
		return self.peer

	def setPeer(self, val):
		self.peer = val

# use these for creating tables.
# if __name__ == '__main__':
# 	database.create_tables([Peer, Payload, Chunk, Logs])