#!/usr/bin/env python
import base64
import json
import urllib, urllib2
from get_credentials import get_api_keys

API_KEY = get_api_keys()['pushbullet']
USER_DATA_URL = 'https://api.pushbullet.com/v2/users/me'
DEVICE_URL = 'https://api.pushbullet.com/v2/devices'
PUSH_URL = 'https://api.pushbullet.com/v2/pushes'

def send_request(url, post_data=None):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (API_KEY, '')).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    if post_data is not None:
        request.data = urllib.urlencode(post_data)
    call = urllib2.urlopen(request)
    result = call.read()
    return json.loads(result)

def get_user_email():
    user_info = send_request(USER_DATA_URL)
    return user_info['email']

def get_device_list():
    return send_request(DEVICE_URL)['devices']

def get_device_by_name(name):
    devices = get_device_list()
    return [i for i in devices if i.get(u'nickname', '') == name][0]

def get_devices_by_type(device_type):
    devices = get_device_list()
    return [i for i in devices if i.get(u'type', '') == device_type]

def send_note(email, title, body, sending_device=None):
    if sending_device is None:
        return send_request(PUSH_URL,
                post_data={'email': email, 'type':'note', 'title': title,
                    'body': body})
    else:
        return send_request(PUSH_URL,
                post_data={'email': email, 'type':'note', 'title': title,
                    'body': body, 'source_device_iden': sending_device})

def send_url(email, title, url, body='', sending_device=None):
    if sending_device is None:
        return send_request(PUSH_URL,
                post_data={'email': email, 'type':'note', 'title': title,
                    'url': url, 'body': body})
    else:
        return send_request(PUSH_URL,
                post_data={'email': email, 'type':'note', 'title': title,
                    'url': url, 'body': body, 'source_device_iden': sending_device})

def get_pushes(modified_after=0):
    return send_request(PUSH_URL + '?modified_after=' + str(modified_after))['pushes']

def filter_pushes(attr, value):
    pushes = get_pushes()
    return [i for i in pushes if i.get(attr, '') == value]

def get_pushes_for_device(dev_name):
    dev_iden = get_device_by_name(dev_name)
    return filter_pushes(u'receiver_iden', dev_iden)

