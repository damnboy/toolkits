#!/usr/bin/python
#coding=utf-8

import urlparse
import random

class UserAgents:
    def __init__(self):
        self.random_user_agents =  ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
                (KHTML, like Gecko) Element Browser 5.0', \
                'Mozilla/5.0 (Macintosh) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4',\
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
                'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
                'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
                Version/6.0 Mobile/10A5355d Safari/8536.25', \
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/28.0.1468.0 Safari/537.36', \
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

    def random(self):
        return self.random_user_agents[random.randint(0,len(self.random_user_agents)-1)]

user_agents = UserAgents()

'''
从dict类型的header中提取响应内容的编码,否则无法解码页面内容
字符
媒体

所否压缩处理
'''
class ContentDecoder:
    def __init__(self):
        self.default_encoding = 'utf-8'

    def detect(self, headers):
        encoding = self.default_encoding
        return encoding

content_decoder = ContentDecoder()

class method:

    def __init__(self):
        self.error = ''

    #def request_and_response(url):

    #def parse_response(url):

    def request(self, url, cookies=''):

        #解析url到成员变量
        ret = urlparse.urlparse(url)

        self.schema = ret[0]
        if self.schema == 'http' :
            self.port = 80
        elif self.schema == 'https':
            self.port = 443

        if ret[1].split(':') == 2:
            self.host, self.port = ret[1].split(':')
        else:
            self.host = ret[1]

        self.path = ret[2]
        self.params = ret[4]
        self.cookies = ''

        self.response = self.request_and_response(url, self.cookies);
        response_data = self.parse_response_data(self.response)
        return response_data


