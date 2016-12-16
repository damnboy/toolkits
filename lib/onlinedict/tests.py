#!/usr/bin/python
#coding=utf-8

from lib.onlinedict.impls.bing import OnlineDictBing

if __name__ == '__main__':
    online_dict = OnlineDictBing()
    pronunciation, explain = online_dict.searchWord('ok')
    print pronunciation
    print explain