def graphCallGen(output, listOfCounts, subsetList):
    """
    Basically gets the required data for the the subset graph and the Pie Charts.
    tbh don't remember how I got this working for the graphCounts
    as look at the amount of abstactions for types and each graph
    but it does work and show all the data based on all my checks.
    """
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
    except StopIteration:
        print("End of Retrieval")
    except Exception as e:
        print("graphCallGen - Major unexpected probaly no entry. Error:", e)

    lists['calls'] = subset_calls
    return lists


def graphFormatter(source):
    """Formats the data as the Pie Chart creator requires for graphing."""
    formatted = []
    for i in source.items():
        formatted.append({
            'label': i[0],
            'data': i[1],
        })

    return formatted
