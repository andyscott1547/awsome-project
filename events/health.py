#!/usr/bin/env python
'''health endpoint for AWSome SAM APP'''

import json

def health_handler(event, context):
    """simple function for basic health check"""
    print(event)
    print(context)

    return {
        "statusCode": 200,
        #'headers': {
        #    'Access-Control-Allow-Headers': '*',
        #    'Access-Control-Allow-Origin': '*',
        #    'Access-Control-Allow-Methods': '*'
        #},
        "body": json.dumps("application health OK")
    }
