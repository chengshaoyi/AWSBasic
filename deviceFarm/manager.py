import ConfigParser
import sys
import os.path
import boto3
import time
import requests
# the configuration file contains
# project
# device-pool
# apk




def parseDFRunConfiguration(confFile):
    config = ConfigParser.ConfigParser()
    config.read(confFile)

def simpleTryAll():
    client = boto3.client('devicefarm')
    prjARN = createDFProject(client,'cliNewPrj2',5)
    devPoolARN = createDevList(client, prjARN)
    apkARN = createAPKUpload(client,prjARN,'app-debug.apk')
    if waitForAPKUpload(client,apkARN):
        pass#scheduleTestRun(client,prjARN,apkARN,devPoolARN,'curTest')
    else:
        print("didnt upload successfully")

    #for curItem in response['projects']:
    #    print(curItem['name'])
    #    print(curItem['arn'])
        
    #    print("----------------")
    #    if(curItem['name'] == 'cliCreated'):
            #response = client.create_device_pool(
            #    name='cliCreatedDevicePool', 
            #    description='Trial Android devices',
            #    projectArn=curItem['arn'],
            #    rules=[platformRule,formFactorRule,makerRule]           
            #)
    #        response = client.create_upload(
    #            projectArn=curItem['arn'],
    #            name='app-debug.apk',
    #            type='ANDROID_APP',
    #            contentType="application/octet-stream"
    #        )
    #        print(response)
    #    else:
    #        print(curItem['name'])



def getARNFromCreateResponse(response,type):
    prjInfo = response[type]
    if prjInfo:
        prjARN = prjInfo['arn']
    return prjARN

def scheduleTestRun(client, prjARN, appARN, poolARN, testName):

    testConfig ={}
    testConfig['type'] = 'BUILTIN_FUZZ'
    testConfig['parameters'] = {
        'event_count': '100',
        'throttle': '50'
    }



    response = client.schedule_run(
        projectArn=prjARN,
        appArn=appARN,
        devicePoolArn=poolARN,
        name='simpleTest',
        test=testConfig,
    )

    print(response)

def waitForAPKUpload(client, appARN):
    timeout = 20
    while True:
        response = client.get_upload(
            arn=appARN
        )
        print(response)
        if response['upload']:
            curStatus = response['upload']['status']
            if(curStatus == 'SUCCEEDED'):
                return 1
        timeout -= 5
        if timeout < 0:
            break
        time.sleep(5)
    return 0



def upload(filename,url):
    with open(filename, 'rb') as f:
        response = requests.put(url=url,data=f)
    print(response.status_code)
    print(response.content)


def createAPKUpload(client, prjARN, path2APK):
    response = client.create_upload(
        projectArn=prjARN,
        name='app-debug.apk',
        type='ANDROID_APP'
    )
    print("APK upload:")
    print(response)
    if response['upload']:
        s3url = response['upload']['url']
        print(s3url)

        upload('./app-debug.apk',s3url)
    return getARNFromCreateResponse(response,'upload')

def createDFProject(client, prjName, timeoutMin):
    response = client.create_project(
        name=prjName,
        defaultJobTimeoutMinutes = timeoutMin
    )
    print("project creation:")
    print(response)
    prjARN = getARNFromCreateResponse(response,'project')
    print(prjARN)
    return prjARN


def createDevList(client, prjARN):
    platformRule = {}
    platformRule['attribute'] = 'PLATFORM'
    platformRule['operator'] = 'EQUALS'
    platformRule['value'] = "\"ANDROID\""

    formFactorRule = {}
    formFactorRule['attribute'] = 'FORM_FACTOR'
    formFactorRule['operator'] = 'EQUALS'
    formFactorRule['value'] = "\"PHONE\""

    makerRule = {}
    makerRule['attribute'] = 'MANUFACTURER'
    makerRule['operator'] = 'EQUALS'
    makerRule['value'] = "\"HTC\""

    response = client.create_device_pool(
        name='cliCreatedDevicePool1',
        description='Trial Android devices',
        projectArn=prjARN,
        rules=[platformRule,formFactorRule,makerRule]
    )
    print("device pool creation:")
    print(response)
    devPoolARN = getARNFromCreateResponse(response,'devicePool')
    return devPoolARN



def deleteProjWithName(prjName):
    client = boto3.client('devicefarm')
    response = client.list_projects()
    for curItem in response['projects']:
        print(curItem['name'])
        print(curItem['arn'])

        print("----------------")
        if(curItem['name'] == prjName):
            client.delete_project(arn=curItem['arn'])
            print(curItem['name']," deleted:", curItem['arn'])
    # response = client.create_device_pool(
    #    name='cliCreatedDevicePool',
    #    description='Trial Android devices',
    #    projectArn=curItem['arn'],
    #    rules=[platformRule,formFactorRule,makerRule]
    # )
    #        response = client.create_upload(
    #            projectArn=curItem['arn'],
    #            name='app-debug.apk',
    #            type='ANDROID_APP',
    #            contentType="application/octet-stream"
    #        )
    #        print(response)
    #    else:
    #        print(curItem['name'])


if __name__ == '__main__':
#    assert(len(sys.argv) >= 2), "Please supply the configuration file for device farm run"
#    assert(os.path.isfile(sys.argv[1])), "Configuration file does not exist"
#    parseDFRunConfiguration(sys.argv[1])
    simpleTryAll()
    #deleteProjWithName('cliNewPrj2')


