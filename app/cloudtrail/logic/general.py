from cloudtrail.models import Searches

#Checks if a search key already exists, returns True or False a result
def searchKeyExists(searchKey):
  try:
    Searches.objects.get(search_key=searchKey)
    return True
  except:
    return False

#Queries the Searches database and returns the ID's in reverse order
def recents():
  return Searches.objects.order_by('id').reverse()

#Returns a dictionary of the relevant details for a search key
def details(searchKey):
  data = Searches.objects.get(search_key=searchKey)

  details = {}
  details['searchKey'] = data.search_key
  details['account'] = data.account
  details['location'] = data.location
  details['dateRun'] = data.search_date
  details['dateFor'] = data.data_date

  return details

#Saves a search into the database
def saveSearch(searchKey, account, data_date):
  entry = Searches(search_key=searchKey,
    account= account, 
    location=searchKey,
    data_date=data_date)
  entry.save()

  return True
