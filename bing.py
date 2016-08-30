# -*- coding: utf-8 -*-
import urllib
import requests
import sys
import api_keys

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
            list[string]
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


if __name__ == '__main__':
    # bing_api.pyを単独で使うと、入力した語で50件検索して結果を表示するツールになる
    for query in sys.stdin:
        bing = Bing()
        results = bing.web_search(query=query, result_num=50, keys=["Title", "Url"])
        print(results)
