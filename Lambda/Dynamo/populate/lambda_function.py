from __future__ import print_function
import urllib
import datetime 
import boto3
from botocore.client import Config


import json

print('Loading function')


def lambda_handler(event, context):

    #populate the model to SoC mapping?    

    #populate the artifact look up
    dynamodb = boto3.client('dynamodb')
    for entry in event.keys():
        curUserContent = event[entry]
        appId = curUserContent['appID']
        item2Upload = {}
        item2Upload['appID'] = {'S':str(appId)}
        appInfo = dynamodb.get_item(TableName ='UserID2NetID2SoCTable', Key={'appID':{'S':str(appId)}}) 
        if appInfo and 'Item' in appInfo:
            print("skip", appId)
            continue
        for netId in curUserContent.keys():
            if netId == 'appID':
                continue
            else:
                soc2globalIDMap = curUserContent[netId]
                map2Upload={}
                for soc, globalID in soc2globalIDMap.iteritems():
                    map2Upload[soc] ={'S': globalID}
                item2Upload[netId] = {'M':map2Upload}
        addResponse = dynamodb.put_item(TableName ='UserID2NetID2SoCTable', Item=item2Upload) 
    
    allStr = ""
    return { 
        "statusCode": 200, "body": allStr
    } 

    
     
    
    


