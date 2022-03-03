import boto
import os
import gzip
import json
import tarfile

import cloudtrail.logic.constants as constants


def cloudtrail_load(searchKey, request):
    """
    Used when a tarball/gzip of the CloudTrail logs is loaded for a search
    """
    try:
        os.mkdir(constants.SEARCH_DIR+'/'+searchKey)
    except OSError as e:
        print("OS Error, likely directory already exists. Error:" + str(e))
    except Exception as e:
        print("cloudtrail_pull - Unexpected error:", e)

    f = request.FILES['file']
    # Writes the .gzip to the search directory
    with open(constants.SEARCH_DIR+'/'+searchKey+'/'+'bundle.tar.gzb', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # Opens the gzip and then outputs the tarball to the same location
    inF = gzip.open(constants.SEARCH_DIR+'/'+searchKey+'/bundle.tar.gzb', 'rb')
    outF = open(constants.SEARCH_DIR+'/'+searchKey+'/bundle.tar', 'wb+')
    outF.write(inF.read())
    inF.close()
    outF.close()

    # Opens the tarball and extracts all the CloudTrail generated .gzip files.
    tar = tarfile.open(constants.SEARCH_DIR+'/'+searchKey+'/bundle.tar')
    tar.extractall(path=constants.SEARCH_DIR+'/'+searchKey)
    tar.close()


def cloudtrail_pull(region, bucket, prefix, output_dir):
    s3conn = boto.s3.connect_to_region(region)
    bucketconn = boto.s3.bucket.Bucket(connection=s3conn, name=bucket)

    try:
        os.mkdir(output_dir)
    except OSError as e:
        print("OS Error, likely directory already exists. Error:" + str(e))
    except Exception as e:
        print("cloudtrail_pull - Unexpected error:", e)

    # Using the providing bucket related information it gets a list of all the objects and then downloads each one of these
    print("Object List:")
    try:
        a = iter(bucketconn.list(prefix=prefix))
        for i in a:
            name = str(str(i.name).split('/')[-1:][0])
            print("Retrieving file: "+i.name + " - Local file name: " + name)
            k = boto.s3.key.Key(bucketconn)
            print("Name: " + name)
            print("Prefix: " + prefix)
            k.key = prefix+name
            k.get_contents_to_filename(output_dir+"/"+name)
    except StopIteration:
        print("End of Retrieval")
    except Exception as e:
        print("cloudtrail_pull - Unexpected error:", e)


def uncompress(files):
    master_file = open(files+'/complete.json', 'w+')

    # Opens each of the CloudTrail .gzip files, reading the contents and then using this as the required data in the complete.json file for the search
    all_records = []
    for file in os.listdir(files):
        if file.endswith(".gz"):
            with gzip.open(files+"/"+file, 'r') as f:
                file_content = f.read()
                data = file_content.decode("utf-8")

                for i in json.loads(data)['Records']:
                    all_records.append(i)

    json.dump(all_records, master_file, indent=4)
    master_file.close()

# Loads the data from the file created in uncompress


def load_data(files):
    master_file = open(files+'/complete.json', 'r')
    data = json.load(master_file)
    master_file.close()
    return data
