from django.conf import settings

#Directory used to store search data
SEARCH_DIR = settings.BASE_DIR+'/searches'

#Cloud Trail items for each API call, used in full_results view
OUTPUT_HEADERS = [
  'awsRegion',
  'eventID',
  'eventName',
  'eventTime',
  'eventType'
  'eventSource',
  'eventVersion',
  'userAgent',
  'requestParameters', 
  'requestID',
  'recipientAccountId',
  'userIdentity',
  'sourceIPAddress',
  'responseElements',
  'errorCode',
  'errorMessage' ]
