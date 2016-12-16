#!/usr/bin/python
#coding=utf-8

from lib.onlinedict.impls.onlinedict import OnlineDict
from urllib import urlencode,quote


class OnlineDictICIBA(OnlineDict):

     def buildSearchUrl(self, word):
        print '\r\n--- from iciba ---'
        return "http://www.iciba.com/"+quote(word)


     def printPronunciation(self, html_content):
        prs = html_content.xpath("//div[@class='base-speak']/span")
        for pr in prs:
            print pr.text,
        print ''

    #<ul class="base-list switch_part">
     def printExplain(self,html_content):
         nodes_word_def = html_content.xpath("//ul[@class='base-list switch_part']/li")
         for node_word_def in nodes_word_def:
             if len(node_word_def.attrib) == 0:
                prop = node_word_def.xpath('./span[@class="prop"]')
                p = node_word_def.xpath('./p')
                if len(prop) and len(p):
                    prop = prop[0].text
                    p = p[0].text.replace('  ','').replace('\r','').replace('\n','')
                    print prop, p

         #<span class="prop chinese">变形</span>
         node_change = html_content.xpath('//div[@class="in-base"]/li[@class="change"]')
         if len(node_change):
            p = node_change[0].xpath('./p')
            if len(p):
                p = p[0].getchildren()
                for index, tag in enumerate(p):
                    print tag.text,
                    if (index+1) % 2 == 0:
                        print ', ',
                print ''
