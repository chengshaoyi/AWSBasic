from __future__ import print_function
import urllib
import datetime 
import boto3
from botocore.client import Config


import json

print('Loading function')

# parsing the event to get the networkId, appId and phoneConfig
# retrieve the S3 file pointer and return a presigned URL, return a response
# REMEMBER: this lambda needs to have a role that can access the S3 bucket
def lambda_handler(event, context):
    phoneConfig = event['queryStringParameters']['phoneConfig']
    netId = event['queryStringParameters']['netId']
    appId = event['queryStringParameters']['appId']
    # from these, find presign a url from S3
    
    #allStr = phoneConfig+" "+netId+" "+appId+"\n"
    print(phoneConfig+" "+netId+" "+appId+"\n")
    BUCKET_NAME = 'shaoyi-s3-log'
    FILE_NAME = "20170928.info";
    s3_client = boto3.client('s3')
        
    url = s3_client.generate_presigned_url('get_object',  Params = {'Bucket': BUCKET_NAME, 'Key': FILE_NAME}, ExpiresIn = 100)
    allStr = url
    return { 
        "statusCode": 200, "body": allStr
    } 

    
     
    
    


