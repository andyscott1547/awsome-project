import json
import pytest
import os
import boto3

from aws_xray_sdk.core import patch_all, xray_recorder
from moto import mock_dynamodb2
from events import health
from events import preflight

"""Unit tests for AWSome SAM App"""

os.environ['TableName'] = 'Dev-Record-Table'
os.environ['AWS_DEFAULT_REGION'] = 'eu-west-2'
AWS_ACCESS_KEY_ID='testing'
AWS_SECRET_ACCESS_KEY='testing'
AWS_SECURITY_TOKEN='testing'
AWS_SESSION_TOKEN='testing'

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "Email": "andyscott1547@hotmail.com","First_Name": "Harry","Surname": "Potter","Contact_Number": "00712345694","House_Number": "hogwarts","Street_Name": "school","Town": "Hogsmede","County": "magical kingdom ","Postcode": "wz1 9hp","Request": "Test","Message": "Test"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "GET",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789022",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"pytest": "mock"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "GET",
        "stageVariables": {"pytest": "mock"},
        "path": "/health",
    }


def test_health_handler(apigw_event, mocker):

    ret = health.health_handler(apigw_event, "")
    data = json.loads(ret["body"])
    print(mocker)

    assert ret["statusCode"] == 200
    assert data == "application health OK"

def test_preflight_handler(apigw_event, mocker):

    ret = preflight.preflight_handler(apigw_event, "")
    data = json.loads(ret["body"])
    print(mocker)

    assert ret["statusCode"] == 200
    assert data == "Preflight check completed OK"

@mock_dynamodb2
def test_create_handler(apigw_event, mocker):
    from events import create

    table_name = 'Dev-Record-Table'
    dynamodb = boto3.resource('dynamodb', 'eu-west-2')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'Email', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'Email','AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    response = create.create_handler(event=apigw_event, context={})

    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'Email': 'andyscott1547@hotmail.com'
        }
    )
    
    item = response['Item']
    resp = item['Email']
    assert resp == 'andyscott1547@hotmail.com'

@mock_dynamodb2
def test_scan_handler(apigw_event, mocker):
    from events import scan
    from events import create

    table_name = 'Dev-Record-Table'
    dynamodb = boto3.resource('dynamodb', 'eu-west-2')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'Email', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'Email','AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    print(table)

    response = create.create_handler(event=apigw_event, context={})
    print(response)
    ret = scan.scan_handler(event=apigw_event, context={})
    print(mocker)

    assert ret["statusCode"] == 200

@mock_dynamodb2
def test_delete_handler(apigw_event, mocker):
    from events import delete
    from events import create

    table_name = 'Dev-Record-Table'
    dynamodb = boto3.resource('dynamodb', 'eu-west-2')

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{'AttributeName': 'Email', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'Email','AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    print(table)

    response = create.create_handler(event=apigw_event, context={})
    print(response)
    ret = delete.delete_handler(event=apigw_event, context={})
    print(mocker)

    assert ret["statusCode"] == 200


