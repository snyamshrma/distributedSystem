from constants import StatusCodes, ResponseFields

class ResponseVariable:
	def __init__(self,name, dtype):
		self.name = name
		self.dtype = dtype
		self.value = None

	def __str__(self):
		return self.name

	def getValue(self):
		return self.value

	def setValue(self,var):
		self.value = var

class JsonResponse:
	def __init__(self):
		pass

	statusCode = ResponseVariable(ResponseFields.STATUS_CODE, 'str')
	message = ResponseVariable(ResponseFields.MESSAGE, 'str')
	errorMessage = ResponseVariable(ResponseFields.ERROR_MESSAGE, 'str')
	data = ResponseVariable(ResponseFields.DATA, 'dict')

	def getStatusCode(self):
		return self.statusCode.getValue()

	def getMessage(self):
		return self.message.getValue()

	def getErrorMessage(self):
		return self.errorMessage.getValue()

	def getData(self):
		return self.data.getValue()

	def setStatusCode(self, var):
		self.statusCode.setValue(var)

	def setMessage(self, var):
		self.message.setValue(var)

	def setErrorMessage(self, var):
		self.errorMessage.setValue(var)

	def setData(self, var):
		self.data.setValue(var)

	def to_json(self):
		if self.statusCode.getValue() == StatusCodes.SUCCESS:
			return {str(self.statusCode):self.statusCode.getValue(), str(self.message):self.message.getValue(),
			        str(self.data):self.data.getValue()}
		else:
			return {str(self.statusCode): self.statusCode.getValue(), str(self.errorMessage): self.errorMessage.getValue()}


def setResponseData(statusCode, message=None, errorMessage=None, jsonData=None):
	jsonResponse = JsonResponse()
	jsonResponse.setData(jsonData)
	jsonResponse.setMessage(message)
	jsonResponse.setErrorMessage(errorMessage)
	jsonResponse.setStatusCode(statusCode)

	return jsonResponse.to_json()
