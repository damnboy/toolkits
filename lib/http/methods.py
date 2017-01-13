from lib.http.methodimpls.impl import implhttplib, implurllib2, implrequests

class HTTPLibrary:
    def __init__(self, dependency):
        if dependency == 'urllib2':
            self._impl_get = implurllib2.get_method_impl_urllib2()
        elif dependency == 'httplib':
            self._impl_get = implhttplib.get_method_impl_httplib()
        elif dependency == 'requests':
            self._impl_get = implrequests.get_method_impl_requests()
            self._impl_transformer = implrequests.impl_request.transformer
        elif dependency == 'pycurl':
            pass
        else:
            print 'unknown http lib'


    def get(self, url):
        return self._impl_get.request(url)

    def transformer(self, fq):
        return self._impl_transformer(fq)

methods = HTTPLibrary('requests')