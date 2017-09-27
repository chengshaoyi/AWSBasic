#!/bin/bash
AWSProfileName="trial0"
# specify your own access key id and secret key
AWSAccessKeyID=""
AWSSecretAccessKey=""
AWSDefaultRegion="us-west-2"
AWSDefaultOutFmt="text"



echo "[profile $AWSProfileName]" > ~/.aws/config
echo "output = $AWSDefaultOutFmt" >> ~/.aws/config
echo "region = $AWSDefaultRegion" >> ~/.aws/config


echo "[$AWSProfileName]" > ~/.aws/credentials
echo "aws_access_key_id = $AWSAccessKeyID" >> ~/.aws/credentials
echo "aws_secret_access_key = $AWSSecretAccessKey" >> ~/.aws/credentials

