#!/usr/bin/env python3
'''Record microservice AWSome builder project'''

import json
import logging
import os
from decimal import Decimal
import boto3

from aws_xray_sdk.core import patch_all, xray_recorder

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

# Convert Decimal to float
class DecimalEncoder(json.JSONEncoder):
    '''Convert decimal to float'''
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)

# Helper class to convert a DynamoDB item to JSON.
#class DecimalEncoder(json.JSONEncoder):
#    '''convert decimal to serialisable JSON'''
#    def default(self, o):
#        if isinstance(o, decimal.Decimal):
#            if o % 1 > 0:
#                return float(o)
#            else:
#                return int(o)
#        return super(DecimalEncoder, self).default(o)

tablename = os.environ['TableName']
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(tablename)

@xray_recorder.capture('sam-app')
def scan_handler(event, context):
    '''default handler'''
    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])


    print (event)
    print (context)
    return {
        'statusCode': 200,
        #'headers': {
        #    'Access-Control-Allow-Headers': '*',
        #    'Access-Control-Allow-Origin': '*',
        #    'Access-Control-Allow-Methods': '*'
        #},
        'body': json.dumps(data, cls=DecimalEncoder)
    }
