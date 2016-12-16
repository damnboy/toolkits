#!/usr/bin/python
#coding=utf-8

from lib.onlinedict.impls.onlinedict import OnlineDict
from urllib import urlencode,quote

class OnlineDictBing(OnlineDict):

    def buildSearchUrl(self, word):
        print '\r\n--- from bing ---'
        #FORM=BDVSP6&mkt=zh-cn
        query_string = {
            'q': word,
            'FORM':'BDVSP6',
            'mkt':'zh-cn'
        }
        return "http://www.bing.com/dict/?"+urlencode(query_string)

    def parsePronunciation(self, html_content):
        pronunciation = u''
        pr_US = html_content.xpath("//div[@class='qdef']/div[@class='hd_area']/div[@class='hd_tf_lh']/div[@class='hd_p1_1']/div[@class='hd_prUS']")
        pr_UK = html_content.xpath("//div[@class='qdef']/div[@class='hd_area']/div[@class='hd_tf_lh']/div[@class='hd_p1_1']/div[@class='hd_pr']")
        if len(pr_US) > 0:
            pronunciation+= pr_US[0].text
        if len(pr_UK) > 0:
            pronunciation+= pr_UK[0].text

        return pronunciation

    '''
    word_type = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='pos']")
    word_def = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='def']/span")
    web_word_type = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='pos_web']")
    web_word_def = html_content.xpath("//div[@class='qdef']/ul/li/span[@class='def']/span")
    '''
    def parseExplain(self,html_content):
        explain = u''
        nodes_word_def = html_content.xpath("//div[@class='qdef']/ul/li")
        for node_word_def in nodes_word_def:
            for node in node_word_def.getchildren():
                if node.attrib['class'].startswith('pos'):
                    explain += node.text
                    explain += u' '
                if node.attrib['class'] == 'def':
                    nodes_def =  node.getchildren();
                    for node_def in nodes_def:
                        explain+= node_def.text
            explain += u'\r\n'

        return explain


