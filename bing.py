# -*- coding: utf-8 -*-
import urllib
import requests
import sys
import os
from webpage import WebPage
import api_keys
import constants

class Bing():
    def __init__(self, api_key=api_keys.BING_API_KEY):
        self.api_key = api_key

    def web_search(self, query, result_num, keys=["Url"], skip=0):
        """
        Args:
            query: string
            result_num: int
            keys: string
                'ID','Title','Description','DisplayUrl','Url' can be described
            skip: int
        Return:
            list[dict[string, string]]
        """
        url = 'https://api.datamarket.azure.com/Bing/Search/Web?'
        # the max number of one response
        max_num = 50
        params = {
            "Query": "'{0}'".format(query),
            "Market": "'ja-JP'"
        }
        # get as json format
        request_url = url + urllib.parse.urlencode(params) + "&$format=json"
        results = []

        # the number of requests
        repeat = int((result_num - skip) / max_num)
        remainder = (result_num - skip) % max_num

        # repeat sending requests with max_num
        for i in range(repeat):
            result = self._hit_api(request_url, max_num, max_num * i, keys)
            results.extend(result)
        # the rest
        if remainder:
            result = self._hit_api(request_url, remainder, max_num * repeat, keys)
            results.extend(result)

        return results

    def _hit_api(self, request_url, top, skip, keys):
        '''
        send request url and get response

        Args:
            request_url:
            top:
            skip:
            keys:
        Return:
            list[dict[string, string]]
        '''
        #the url sended at last
        final_url = "{0}&$top={1}&$skip={2}".format(request_url, top, skip)
        response = requests.get(final_url,
                                auth=(self.api_key, self.api_key),
                                headers={'User-Agent': 'My API Robot'}).json()
        results = []
        # get selected information
        for item in response["d"]["results"]:
            result = {}
            for key in keys:
                result[key] = item[key]
            results.append(result)
        return results

    def fetch_web_pages(self, query):
        if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
            os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
        os.chdir(constants.FETCHED_PAGES_DIR_NAME)

        results = self.web_search(query=query, result_num=constants.NUM_OF_FETCHED_PAGES, keys=['Url'])
        for i, result in enumerate(results):
            page = WebPage(result['Url'])
            page.fetch_html()
            page.remove_html_tags()
            f = open('%s_%s.html' % (query, str(i)), 'w')
            f.write(page.html_body)
            f.close()

if __name__ == '__main__':
    # bing_api.pyを単独で使うと、入力した語で50件検索して結果を表示するツールになる
    for query in sys.stdin:
        bing = Bing()
        bing.fetch_web_pages(query)
        # results = bing.web_search(query=query, result_num=100, keys=["Title", "Url"])
        # # print(len(results))
        # print(results)
