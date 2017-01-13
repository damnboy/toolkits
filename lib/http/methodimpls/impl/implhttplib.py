#!/usr/bin/python
#coding=utf-8

'''
it only has predictable results for tasks that involve a single socket operation.
An HTTP request consists of multiple socket operations
(e.g. DNS requests or other things that might be abstracted away from an HTTP client).
The timeout of the overall operation becomes unpredictable because of that.

It's because the HTTP spec does not provide anything for the client to specify time-to-live information with a HTTP request.
You can do this only on TCP level, as you mentioned.

On the other hand, the server may inform the client about timeout situations with HTTP status codes
408 Request Timeout resp.
504 Gateway Timeout.
'''

import socket
import httplib
from lib.http.methodimpls.impl.method import user_agents, content_decoder, method


class method_impl_httplib(method):

    def __init__(self):
        method.__init__(self)


    #def custom_request_header(self, cookies):


    #def custom_request_body(self):


    #def custom_request_method(self):


    #TODO
    #if self.schema == 'https' with HTTPSConnection
    #HTTPConnection中包含socket.getaddrinfo的域名解析调用
    #该调用不参与超时部分计算
    #
    def request_and_response(self, url):

        try:
            http_conn = httplib.HTTPConnection(self._host, self._port)
            socket.setdefaulttimeout(self._timeout)
            http_conn.request(self.custom_request_method(),
                              (self._path + '?' + self._params),
                              self.custom_request_body(),
                              self.custom_request_header(self._cookies))

            response = http_conn.getresponse()

        except socket.timeout as e:
            raise e

        return response

    def parse_response(self, response):
        response_data = response.read()
        return response.status, response.msg, response_data.decode(content_decoder.detect(response.msg.dict))



class get_method_impl_httplib(method_impl_httplib):
    def __init__(self):
        method_impl_httplib.__init__(self)

    def custom_request_method(self):
        return 'GET'

    def custom_request_header(self, cookies):
        return {
            'User-Agent' : user_agents.random()
        }

    def custom_request_body(self):
        return None


if __name__ == '__main__':
    method = get_method_impl_httplib()
    method.request('http://www.baidu.com/path/okok.jsp?p1=1')
