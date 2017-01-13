#!/usr/bin/python
#coding=utf-8


import time
def current_time() :
    return time.strftime('_%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))


#http://blog.xiayf.cn/2013/01/26/python-string-format/
class StringGenerator:
    @staticmethod
    def general_format_seq_string(format, start, end):
        ret = []
        for i in range(start, end):
            ret.append(format.format(i))

        return ret

    @staticmethod
    def general_zero_prefix_seq_string(width, start, end):
        format = '{:0>%dd}'% (width)
        return StringGenerator.general_format_seq_string(format, start, end)

    @staticmethod
    def general_seq_string(width, start, end):
        format = '{0}'
        return StringGenerator.general_format_seq_string(format, start, end)


if __name__ == '__main__':
    print StringGenerator.general_seq_string(4, 1, 1000)