#!/usr/bin/env python
from ConfigParser import ConfigParser


def get_api_keys(credentials_file=None):
    """Get API keys for apps that need only a single value to authenticate
    """
    ini_parser = ConfigParser()
    if credentials_file is None:
        ini_parser.read('api_keys.ini')
    else:
        ini_parser.read(credentials_file)
    ans = {}
    for section in ini_parser.sections():
        ans[section] = ini_parser.get(section, 'key')
    return ans

