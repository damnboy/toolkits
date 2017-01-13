#!/usr/bin/python
#coding=utf-8


import requests
from lib.http.methodimpls.impl.method import user_agents, content_decoder, method


class method_impl_requests(method):

    def __init__(self):
        method.__init__(self)


'''
If a response contains some Cookies, you can quickly access them:

>>> url = 'http://example.com/some/cookie/setting/url'
>>> r = requests.get(url)

>>> r.cookies['example_cookie_name']
'example_cookie_value'
To send your own cookies to the server, you can use the cookies parameter:

>>> url = 'http://httpbin.org/cookies'
>>> cookies = dict(cookies_are='working')

>>> r = requests.get(url, cookies=cookies)
>>> r.text
'{"cookies": {"cookies_are": "working"}}'
Cookies are returned in a RequestsCookieJar, which acts like a dict but also offers a more complete interface, suitable for use over multiple domains or paths. Cookie jars can also be passed in to requests:

>>> jar = requests.cookies.RequestsCookieJar()
>>> jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
>>> jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
>>> url = 'http://httpbin.org/cookies'
>>> r = requests.get(url, cookies=jar)
>>> r.text
'{"cookies": {"tasty_cookie": "yum"}}'
'''
class get_method_impl_requests(method_impl_requests):
    def __init__(self):
        method_impl_requests.__init__(self)

    def request_and_response(self, url):

        try:
            return requests.get(url, timeout = self._timeout)

        except requests.ConnectTimeout:
            raise RuntimeError('requests.ConnectTimeout')

    '''
        response.text会解码body内容,存在一定开销
        apparent_encoding 会调用编码检测lib, 尝试检测html页面中文字的编码,开销较大
    '''
    def parse_response(self, response):
        return response.status_code, response.headers, response.content.decode(response.apparent_encoding)



class impl_request(method_impl_requests):

    def __init__(self, request, timeout):
        method_impl_requests.__init__(self)
        self._request = request
        self._timeout = timeout

    def make_request_and_wait_response(self):

        try:
            s = requests.Session()
            return s.send(self._request,
                          timeout = self._timeout,
                          allow_redirects = False,
                          verify = False)

        except requests.ConnectTimeout as e:
            raise RuntimeError('conn timeout')
        except requests.ConnectionError as e:
            raise RuntimeError('conn error')
        except requests.ReadTimeout as e:
            raise RuntimeError('read timeout')

    '''
        response.text会解码body内容,存在一定开销
        apparent_encoding 会调用编码检测lib, 尝试检测html页面中文字的编码,开销较大
    '''
    def parse_response(self, response):
        content = response.content
        if len(content) != 0:
            encoding = response.apparent_encoding
            if encoding == None:
                encoding = self._prefer_encoding
            content = content.decode(encoding)

        return response.status_code, response.headers, content


    @staticmethod
    def transformer(fuzz_request):
        data = None
        auth = None
        if(fuzz_request.method in ['POST', 'PUT']):
            data = fuzz_request.postdata

        if(fuzz_request.getAuth()):
            auth = None

        req = requests.Request(
            method = fuzz_request.method,
            url = fuzz_request.completeUrl,
            headers = fuzz_request._headers,
            data = data,
            auth = auth)

        return impl_request(req.prepare(), fuzz_request.getConnTimeout())


if __name__ == '__main__':
    method = get_method_impl_requests()
    method.request('http://www.baidu.com/path/okok.jsp?p1=1')