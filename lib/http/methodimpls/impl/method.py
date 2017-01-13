#!/usr/bin/python
#coding=utf-8

import urlparse
import random
import config.encoding
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
        self._prefer_encoding = config.encoding.default_os_encoding
        self._error = None
        self._timeout = 5
        self._cookies = ''
        self._code = -1
        self._response_header = {}
        self._response_body = u''


    #def request_and_response(url):

    #def parse_response(url):

    def make_request(self):
        try:
            self._response = self.make_request_and_wait_response();

            self._code, self._response_header, self._response_body = self.parse_response(self._response)

        except UnicodeDecodeError as e:
            raise e

        return self
'''
    #返回
    # status code(int)
    # header(dict)
    # body(unicode)
    def request(self, url):

        #解析url到成员变量
        ret = urlparse.urlparse(url)

        self._schema = ret[0]
        if self._schema == 'http' :
            self._port = 80
        elif self._schema == 'https':
            self._port = 443

        if ret[1].split(':') == 2:
            self._host, self._port = ret[1].split(':')
        else:
            self._host = ret[1]

        self._path = ret[2]
        self._params = ret[4]


        #包装以下各个lib的异常,统一raise
        try:
            self._response = self.request_and_response(url);

            self._code, self._response_header, self._response_body = self.parse_response(self._response)

        except Exception as e:
            self._error = e

        return self
'''
