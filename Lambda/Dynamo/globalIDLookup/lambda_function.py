from __future__ import print_function
import urllib
import datetime 
import boto3
from botocore.client import Config
import json

print('Loading function')

# parsing the event to get the networkId, appId and phoneConfig
# retrieve the S3 file pointer and return a presigned URL, return a response

print('Loading function')


def getSoCName(phoneConfig, dynamodb):
    defaultSoC='default'
    soc = dynamodb.get_item(TableName ='PhoneModel2SoC', Key={'model':{'S':str(phoneConfig)}})    
    resultSoC = defaultSoC
    if('Item' in soc):
        if('soc' in soc['Item']):
            item = soc['Item']['soc']
            resultSoC = item['S']
    return resultSoC

def extractIDFromItem(appInfoItem, netId, soc):
    if(netId in appInfoItem):
        soc2gIDMap = appInfoItem[netId]
        if(soc in soc2gIDMap['M']):
            globalID = soc2gIDMap['M'][soc]['S']
            return globalID
    return None

def getGlobalID(soc, appId, netId, dynamodb):
    globalID = None
    # look for netID, and check to see if the json has the particular model    
    appInfo = dynamodb.get_item(TableName ='UserID2NetID2SoCTable', Key={'appID':{'S':str(appId)}}) 
    if(appInfo and 'Item' in appInfo):
        appInfoItem = appInfo['Item']
        globalID = extractIDFromItem(appInfoItem, netId, soc)
    else:
        appInfo = dynamodb.get_item(TableName ='UserID2NetID2SoCTable', Key={'appID':{'S':str('public')}}) 
        appInfoItem = appInfo['Item']
        globalID = extractIDFromItem(appInfoItem, netId, soc)
        
    return globalID
    
def lambda_handler(event, context):
    phoneConfig = event['queryStringParameters']['phoneConfig']
    netId = event['queryStringParameters']['netId']
    appId = event['queryStringParameters']['appId']
    # look for the global ID with the phoneConfig and netID    
    # look for the SoC from a phoneConfig
    dynamodb = boto3.client('dynamodb')
    resultSoC = getSoCName(phoneConfig, dynamodb)
    
    globalID = getGlobalID(resultSoC, appId, netId, dynamodb)                
    if(globalID):    
        return { 
            "statusCode": 200, "body": "{\"globalNNIdStr\": \""+globalID+"\", \"lastModified\":10}"
        }
    else: # this would send back an error response
        raise Exception('global id not found')

    


#def lambda_handler(event, context):
#    print(event)
#    phoneConfig = event['queryStringParameters']['phoneConfig']
#    netId = event['queryStringParameters']['netId']
#    appId = event['queryStringParameters']['appId']
    # from these, search for globalId in dynamoDB
    
#    allStr = phoneConfig+" "+netId+" "+appId+"\n"
#    print(allStr)
#    return { 
#        "statusCode": 200, "body": "{\"globalNNIdStr\": \"dummyTest\", \"lastModified\":10}"
#    } 
    
