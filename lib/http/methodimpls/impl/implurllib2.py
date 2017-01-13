#!/usr/bin/python
#coding=utf-8
import socket
import urllib2
from lib.http.methodimpls.impl.method import user_agents, content_decoder, method


class method_impl_urllib2(method):

    def __init__(self):
        method.__init__(self)

    def request_and_response(self, url):

        try:
            request = urllib2.Request(url)
            request = self.custom_request(request)
            opener = urllib2.build_opener()
            #open重写了timeout参数
            response = opener.open(request, timeout = self._timeout)

        except urllib2.URLError as e:
            if isinstance(e.reason, socket.timeout):
                raise RuntimeError('timeout')
            else:
                raise e

        return response

    def parse_response(self, response):
        response_data = response.read()
        return response.code, response.headers, response_data.decode(content_decoder.detect(response.headers.dict))


class get_method_impl_urllib2(method_impl_urllib2):

    def __init__(self):
         method_impl_urllib2.__init__(self)

    def custom_request(self, request):
        request.add_header('User-Agent', user_agents.random())
        request.get_method = lambda: 'GET'
        return request




if __name__ == '__main__':
    method = get_method_impl_urllib2()
    method.request('https://www.baidu.com/path/okok.jsp?p1=1')