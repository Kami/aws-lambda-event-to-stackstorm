# -*- coding: utf-8 -*-
# Copyright 2019 Tomaz Muraus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import logging

import requests


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG = logging.getLogger()
LOG.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', '5'))
VERIFY_SSL_CERT = os.environ.get('VERIFY_SSL_CERT', 'true') == 'true'


def send_event_to_stackstorm(event, context):
    """
    Lambda event handler which sends event objects to StackStorm using StackStorm webhook API
    endpoint.
    """
    LOG.debug('Received event: %s' % (str(event)))

    # Your code goes here!
    webhook_url = os.environ['STACKSTORM_API_URL']

    LOG.info('Sending event to StackStorm webhook endpoint: %s' % (webhook_url))

    headers = {
        'Content-Type': 'application/json',
        'St2-Api-Key': os.environ['STACKSTORM_API_KEY']
    }
    data = json.dumps(event)

    try:
        resp = requests.post(webhook_url, data=data, headers=headers, verify=VERIFY_SSL_CERT,
                             timeout=REQUEST_TIMEOUT)
    except Exception:
        LOG.exception('Failed to send event to StackStorm webhook endpoint')
        return ''

    if resp.status_code != 202:
        LOG.error('Failed to send event to StackStorm webhook endpoint: %s' % (resp.text))
        return ''

    LOG.info('Event sent to StackStorm webhook endpoint: %s' % (webhook_url))

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Event sent to StackStorm'})
    }
