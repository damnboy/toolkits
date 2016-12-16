from lib.http.methodimpls.impl import implhttplib, implurllib2, implrequests

class Methods:
    def __init__(self, dependency):
        if dependency == 'urllib2':
            self.impl_get = implurllib2.get_method_impl_urllib2()
        elif dependency == 'httplib':
            self.impl_get = implhttplib.get_method_impl_httplib()
        elif dependency == 'requests':
            self.impl_get = implrequests.get_method_impl_requests()

    def get(self, url):
        return self.impl_get.request(url)


methods = {
    'requests' : Methods('requests'),
    'urllib2' : Methods('urllib2'),
    'httplib' : Methods('httplib')
}