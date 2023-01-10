#!/usr/bin/env python3

import json
import boto3
import random
import string
from datetime import date

client = boto3.client('codeguru-reviewer')

today = date.today()
date = today.strftime("%b-%d-%Y")


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str

def lambda_handler(event, context):
    commitid = event['Records'][0]['codecommit']['references'][0]['commit']
    response = client.create_code_review(
        Name=f"{date}-AB-Static-Code-Review-{commitid}",
        RepositoryAssociationArn='arn:aws:codeguru-reviewer:eu-west-2:268321956184:association:5d95599c-b0d3-4d54-950e-ca3f1c7767c1',
        Type={
            'RepositoryAnalysis': {
                'RepositoryHead': {
                    'BranchName': 'master'
                }
            }
        },
        ClientRequestToken=f"{get_random_string(8)}"
    )
    # TODO implement
    print (response)
