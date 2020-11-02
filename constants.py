class StatusCodes:
	SUCCESS = 200
	BAD_REQUEST = 400
	INVALID_CREDENTIALS = 401
	SESSION_TIMEOUT = 408
	INTERNAL_SERVER_ERROR = 500
	FORBIDDEN_ACCESS = 403
	INCORRECT_DATE = 50

class ResponseFields:
	STATUS_CODE = 'statusCode'
	MESSAGE = 'message'
	ERROR_MESSAGE = 'errorMessage'
	DATA = 'data'

class PeerType:
	SERVER = 'server'
	PEER = 'peer'

class Activity:
	CLAIMS_EXCHANGED = 'claimsExchanged'
	CLAIMS_RESPONSE = 'claimsResponse'
	COMMS_WITH_TRUSTED_SERVER = 'communicationWithTrustedServer'
