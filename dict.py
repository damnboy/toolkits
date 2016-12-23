#!/opt/local/bin/python
#coding=utf-8

from lib.onlinedict.impls.bing import OnlineDictBing
from config.encoding import default_os_encoding
from lib.utils import *
import pyexcel_ods

if __name__ == '__main__':

    print '---------------------------'
    print 'welcome to online dict v0.1'
    print '---------------------------'

    online_dict = [OnlineDictBing()]
    results = {
        'iciba' : [],
        'bing' : []
    }

    try:

        while True:
            word = raw_input('Any words you don`t know yet? ')

            #url中的编码由urlencoding负责处理
            pronunciation, explain = online_dict[0].searchWord(word)
            if len(pronunciation) == 0 and len(explain) == 0:
                print 'no results'
            else:
                print pronunciation.encode(default_os_encoding)
                print explain.encode(default_os_encoding)
                results['bing'].append([
                    word.decode(default_os_encoding),
                    pronunciation,
                    explain])

        ods_name = '../output/dict/dict' + current_time() + '.ods'
        print '\r\nsaving search results to ' + ods_name + '...',
        pyexcel_ods.write_data(ods_name, results)
        print ('\r\n%d words saved!' % (len(results['bing'])))

    except KeyboardInterrupt as e:
        pass

    except IOError as e:
        print e

