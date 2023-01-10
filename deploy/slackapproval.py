'''CICD Apporval notification to slack'''
import json
import logging
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']
SLACK_CHANNEL = os.environ['slackChannel']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    '''Slack notification'''
    print (context)
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))


    link = message['consoleLink']
    name = message['approval']['pipelineName']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': "Approval required for %s, please follow link to review: %s" % (name, link)
    }

    req = Request(ENCRYPTED_HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
