# -*- coding: utf-8 -*-
import urllib
import lxml.html
import requests
import sys
import os
from webpage import WebPage
import api_keys
import constants
from time import sleep

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

    def get_tabelog_reviews(self, query, result_num=10):
        query = query + ' site:tabelog.com -site:tabelog.com/matome'
        urls = self.web_search(query, result_num, keys=["Url"], skip=0)
        reviews = []
        for url in urls:
            html = requests.get(url['Url']).text
            sleep(2)
            root = lxml.html.fromstring(html)
            try:
                reviwe = root.cssselect('.rvw-item__rvw-title')[0].text_content()
                reviwe += root.cssselect('.rvw-item__rvw-comment > p')[0].text_content()
                reviews.append(reviwe)
            except:
                continue

        return reviews


    def fetch_web_pages(self, query):
        # if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        #     os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
        # os.chdir(constants.FETCHED_PAGES_DIR_NAME)

        results = self.web_search(query=query, result_num=constants.NUM_OF_FETCHED_PAGES, keys=['Url'])
        for i, result in enumerate(results):
            page = WebPage(result['Url'])
            page.fetch_html()
            page.remove_html_tags()
            f = open('./fetched_pages/%s_%s.txt' % (query, str(i)), 'w')
            f.write(page.html_body)
            f.close()

if __name__ == '__main__':

    action_list = []
    f = open('./actions.txt', 'r')
    for line in f:
        action = line.replace('\n', '')
        action = '"' + action + '"'
        action_list.append(action)
    f.close()

    exit()
    
    bing = Bing()
    index = 0
    all_texts = ""
    for action in action_list:
        results = bing.get_tabelog_reviews(action, 50)
        texts = ""
        for result in results:
            text = result.replace('\n', '')
            # print(result)
            texts += text + '\n'
        f = open('./docs/tabelog/0_%s.txt' % (str(index)), 'w')
        f.write(texts)
        f.close()
        print(index)
        index += 1
        all_texts += texts

    fa = open('./docs/tabelog/0_all.txt', 'w')
    fa.write(all_texts)
    fa.close()
    exit()

    bing = Bing()
    results = bing.get_tabelog_reviews('ちょっと飲む', 10)
    for result in results:
        print(result)
    exit();
    # bing.fetch_web_pages(query)
    action_list = []
    f = open('./actions.txt', 'r')
    for line in f:
        action = line.replace('\n', '')
        action = action
        action_list.append(action)
    f.close()
    exit()
    index = 0
    all_texts = ""
    for action in action_list:
        results = bing.web_search(query=action, result_num=500, keys=["Title", "Description"])
        texts = ""
        for dic in results:
            texts += dic['Title'] + dic['Description'] + '\n'
        f = open('./docs/1_%s.txt' % (str(index)), 'w')
        f.write(texts)
        f.close()
        print(index)
        index += 1
        all_texts += texts

    fa = open('./docs/1_all.txt', 'w')
    fa.write(all_texts)
    fa.close()

    # results = bing.web_search(query=query, result_num=500, keys=["Title", "Description"])
    # texts = ""
    # for dic in results:
    #     texts += dic['Title'] + dic['Description'] + '\n'
    # f = open('./docs/%s.txt' % (query), 'w')
    # f.write(texts)
    # f.close()
