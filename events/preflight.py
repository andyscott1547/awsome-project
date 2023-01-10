#!/usr/bin/env python
'''preflight endpoint for AWSome SAM APP'''

import json

def preflight_handler(event, context):
    """simple function for preflight check"""
    print(event)
    print(context)

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'

        },
        "body": json.dumps("Preflight check completed OK")
    }
