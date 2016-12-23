#!/usr/bin/python
#coding=utf-8


import time
def current_time() :
    return time.strftime('_%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))