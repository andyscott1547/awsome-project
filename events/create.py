#!/usr/bin/env python
'''Record microservice AWSome builder project'''

import json
import logging
import os
import boto3
from aws_xray_sdk.core import patch_all, xray_recorder

tablename = os.environ['TableName']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(tablename)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

@xray_recorder.capture('sam-app')
def create_handler(event, context):
    '''Parses JSON body from payload and writes to dynamodb table'''
    response = (event['body'])
    items = json.loads(response)

    table.put_item(
        Item={
            "Email": items['Email'],
            "First_name": items['First_Name'],
            "Surname": items['Surname'],
            "Contact_Number": items['Contact_Number'],
            "House_Number": items['House_Number'],
            "Street_Name": items['Street_Name'],
            "Town": items['Town'],
            "County": items['County'],
            "Postcode": items['Postcode'],
            "Request": items['Request'],
            "Message": items['Message']
        }
    )
    print (event)
    print (context)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps('Your request was successfully submitted.')
    }
