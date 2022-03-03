from cloudtrail.models import Searches


def searchKeyExists(searchKey):
    """Checks if a search key already exists, returns True or False a result."""

    try:
        Searches.objects.get(search_key=searchKey)
        return True
    except:
        return False


def recents():
    """Queries the Searches database and returns the ID's in reverse order."""
    return Searches.objects.order_by('id').reverse()


def details(searchKey):
    """Returns a dictionary of the relevant details for a search key."""
    data = Searches.objects.get(search_key=searchKey)

    details = {
        'searchKey':     data.search_key,
        'account':    data.account,
        'location':     data.location,
        'dateRun':    data.search_date,
        'dateFor':    data.data_date,
    }

    return details


def saveSearch(searchKey, account, data_date):
    """Saves a search into the database."""
    entry = Searches(search_key=searchKey,
                     account=account,
                     location=searchKey,
                     data_date=data_date)
    entry.save()

    return True
