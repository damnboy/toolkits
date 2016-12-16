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

    def request_and_response(self, url, cookies):
        return requests.get(url)

    def parse_response_data(self, response):
        return response.text

if __name__ == '__main__':
    method = get_method_impl_requests()
    method.request('http://www.baidu.com/path/okok.jsp?p1=1')