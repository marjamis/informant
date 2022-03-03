from django.shortcuts import render
from cloudtrail.forms import TimeForm, LocationForm

import cloudtrail.logic.cloudtrail_util as cloudtrailUtil
import cloudtrail.logic.view_generation as viewGeneration
import cloudtrail.logic.general as general
import cloudtrail.logic.constants as constants

import sys
from datetime import datetime


def index(request):
    timeform = TimeForm()
    locationform = LocationForm()
    return render(request, 'public/index.html', {'timeform': timeform,
                                                 'locationform': locationform, 'recent_searches': general.recents()})


def results(request):
    # prev key for returning data from previously created searches
    if "prev" in request.GET:
        searchKey = request.GET['prev']
    # load key for when a gzip/tarball of the CloudTrail logs are provided
    elif "load" in request.POST:
        searchKey = request.POST['load']

        # Checks to make sure the key hasn't been previously used
        if general.searchKeyExists(searchKey):
            return render(request, 'public/error.html', {"message": "Key already exists. Go back and select a unique key."})

        general.saveSearch(searchKey, '-1', datetime.now())
        cloudtrailUtil.cloudtrail_load(searchKey, request)
        cloudtrailUtil.uncompress(constants.SEARCH_DIR+'/'+searchKey)
    # search_key key for when a pull from the S3 for CloudTrail logs is required, uses the passed on details to do this
    elif "search_key" in request.GET:
        searchKey = request.GET["search_key"]

        # Checks to make sure the key hasn't been previously used
        if general.searchKeyExists(searchKey):
            return render(request, 'public/error.html', {"message": "Key already exists. Go back and select a unique key."})

        general.saveSearch(request.GET["search_key"], request.GET["accountId"], datetime.strptime(
            request.GET['date'], "%Y/%m/%d"))
        cloudtrailUtil.cloudtrail_pull(request.GET["bucket_region"],
                                       request.GET['bucket'],
                                       request.GET['prefix']+'AWSLogs/'+request.GET["accountId"] +
                                       '/CloudTrail/us-west-2/' +
                                       request.GET['date']+'/',
                                       constants.SEARCH_DIR+'/'+searchKey)
        cloudtrailUtil.uncompress(constants.SEARCH_DIR+'/'+searchKey)
    else:
        return render(request, 'public/error.html', {"message": sys.exc_info()[0]})

    # Uses the CloudTrail raw JSON data to generate graphs and tables relating to the API calls in the data
    output = cloudtrailUtil.load_data(constants.SEARCH_DIR+'/'+searchKey)
    # A List of the subset of API calls listed in the Results page. Configured in a list for easy add or removing if required
    subsetList = ["eventTime", "eventName", "userAgent"]
    # A list of the graphs that will be generated from the data. NOTE: If these are changed(mainly added/removed) make sure the required changes on the results template are made for viewing
    graphList = ['eventName', 'eventSource', 'userAgent', 'awsRegion']
    # Using the CloudTrail JSON logs generates the required graphs and dictionary of the subset of API calls
    dataCounted = viewGeneration.graphCallGen(output, graphList, subsetList)

    # Returns all the relevant data to the Template
    return render(request, 'public/results.html', {'details': general.details(searchKey),
                                                   'subset_headers': subsetList,
                                                   'subset_calls':  dataCounted['calls'],
                                                   'pieData': [viewGeneration.graphFormatter(dataCounted['eventName']),
                  viewGeneration.graphFormatter(dataCounted['eventSource']),
                  viewGeneration.graphFormatter(dataCounted['userAgent']),
                  viewGeneration.graphFormatter(dataCounted['awsRegion'])
                  ]})


def full_results(request):
    try:
        return render(request, 'public/full_results.html', {'outputHeaders': constants.OUTPUT_HEADERS,
                                                            'output': (cloudtrailUtil.load_data(constants.SEARCH_DIR+'/'+request.GET["prev"]))})
    except Exception as e:
        return render(request, 'public/error.html', {"message": e})


def raw_data(request):
    try:
        return JsonResponse(cloudtrailUtil.load_data(constants.SEARCH_DIR+"/"+request.GET["prev"]), safe=False)
    except Exception as e:
        return render(request, 'public/error.html', {"message": e})
