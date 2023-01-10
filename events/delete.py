#!/usr/bin/env python3
'''Record microservice AWSome builder project'''

import json
import os
import logging
import boto3
from aws_xray_sdk.core import patch_all, xray_recorder

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

tablename = os.environ['TableName']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(tablename)

@xray_recorder.capture('sam-app')
def delete_handler(event, context):
    '''default handler'''
    response = (event['body'])
    items = json.loads(response)
    email = items['Email']

    response = table.delete_item(Key={
        "Email": email
    })

    print (event)
    print (context)
    return {
        'statusCode': 200,
        #'headers': {
        #    'Access-Control-Allow-Headers': '*',
        #    'Access-Control-Allow-Origin': '*',
        #    'Access-Control-Allow-Methods': '*'
        #},
        'body': json.dumps('The record for %s was successfully deleted.' % (email))
    }
