from __future__ import print_function
import urllib
import datetime 
import boto3
from botocore.client import Config

import json

print('Loading function')


def lambda_handler(event, context):
    cur_dt = datetime.datetime.today().strftime('%Y%m%d')
    #retrieve a file
    dls = "http://www.eecs.berkeley.edu/~chengs/.info"
    (filename,headers) = urllib.urlretrieve(dls, cur_dt + ".info")
    print(filename)
    s3_client = boto3.client('s3')

    BUCKET_NAME = 'shaoyi-cheng-test'
    FILE_NAME = cur_dt + ".info";

    data = open(filename, 'r')
    s3_client.put_object(ACL='private', Key=FILE_NAME, Body=data, Bucket=BUCKET_NAME)
    #put a identification in the dynamoDB identifying the file we have uploaded

    #invoke 
    
    


