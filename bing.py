# -*- coding: utf-8 -*-
import urllib
import requests
import sys
import api_keys

class Bing():
    def __init__(self, api_key=api_keys.BING_API_KEY):
        self.api_key = api_key
