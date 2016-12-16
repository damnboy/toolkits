#!/usr/bin/python
#coding=utf-8

from lxml import html
from lib.http.methods import methods

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

            unicode_response = methods['requests'].get(search_url)
            dom_response = html.fromstring(unicode_response)

            pronunciation = self.parsePronunciation(dom_response)
            explain = self.parseExplain(dom_response)

        except Exception as e:
            raise e

        return pronunciation, explain