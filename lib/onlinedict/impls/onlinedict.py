#!/usr/bin/python
#coding=utf-8

from lxml import html
from lib.http.methods import methods
from submodules.wfuzz.framework.fuzzer.fuzzobjects import FuzzRequest
class OnlineDict:
    def __init__(self):
        ''

    def buildSearchUrl(self, word):
        'over write this in subclass'

    def parsePronunciation(self, dom_response):
        'over write this in subclass'

    def parseExplain(self,dom_response):
        'over write this in subclass'

    def searchWord(self, word):

        try:
            search_url = self.buildSearchUrl(word)
            fq = FuzzRequest()
            fq.setUrl(search_url)
            method = methods.transformer(fq)
            unicode_response = method.make_request()
            dom_response = html.fromstring(unicode_response._response_body)

            pronunciation = self.parsePronunciation(dom_response)
            explain = self.parseExplain(dom_response)

        except Exception as e:
            raise e

        return pronunciation, explain