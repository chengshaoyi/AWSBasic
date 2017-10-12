from __future__ import print_function
import urllib
import datetime 
import boto3
from botocore.client import Config


import json

print('Loading function')


def getSoCName(phoneConfig, dynamodb):
    defaultSoC='default'
    soc = dynamodb.get_item(TableName ='PhoneModel2SoC', Key={'model':{'S':str(phoneConfig)}})    
    resultSoC = defaultSoC
    if('Item' in soc):
        item = soc['Item']['soc']
        resultSoC = item['S']
    return resultSoC


def getGlobalID(soc, appId, netId, dynamodb):
    globalID = none
    # look for netID, and check to see if the json has the particular model    
    appInfo = dynamodb.get_item(TableName ='UserID2NetID2SoCTable', Key={'appID':{'S':str(appId)}}) 
    if('Item' in appInfo):
        if(netId in appInfo['Item']):
            soc2gIDMap = appInfo['Item'][netId]
            print(soc2gIDMap)
            if(soc in soc2gIDMap['M']):
                globalID = soc2gIDMap['M'][soc]['S']
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
    else:
        raise Exception('global id not found')

    
     
    
    


