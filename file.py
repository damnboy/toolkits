#!/usr/bin/env python
#coding=utf-8


'''
a regular Python file object that accepts 8-bit strings is returned.
'''
import codecs
f1 = codecs.open('test.txt', encoding='gbk')

f = open('test.txt', 'rb')
lines= f.readlines()
for line in lines:
    print line.decode('utf-8')
f.close()