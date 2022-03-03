import datetime, sys

from cloudtrail.models import Searches

#Basically gets the required data for the the subset graph and the Pie Charts.
#tbh don't remember how I got this working for the graphCounts
#as look at the amount of abstactions for types and each graph
#but it does work and show all the data based on all my checks.
def graphCallGen(output, listOfCounts, subsetList):
  lists = {}
  for i in listOfCounts:
    lists[i] = {}

  try:
    a = iter(output)
    subset_calls = []
    for i in a:
      item = []
      for j in subsetList:
        item.append(i[j])
      subset_calls.append(item)

      for x in listOfCounts:
        try:
          if i[x] in lists[x]:
            lists[x][i[x]] += 1
          else:
            lists[x][i[x]] = 1
        except Exception as e:
          print("graphCallGen - Unexpected probaly no entry. Error:", e)
  except StopIteration as e:
    print("End of Retrieval")
  except Exception as e:
    print("graphCallGen - Major unexpected probaly no entry. Error:", e)

  lists['calls'] = subset_calls
  return lists

#Formats the data as the Pie Chart creator requires for graphing
def graphFormatter(source):
  formatted = []
  for i in source.items():
    item = {}
    item['label'] = i[0]
    item['data'] = i[1]
    formatted.append(item)

  return formatted
