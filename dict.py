#!/opt/local/bin/python
#coding=utf-8

from lib.onlinedict.impls.bing import OnlineDictBing
from config.encoding import default_os_encoding

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
            result = {
                'word' : raw_input('Any words you don`t know yet? ').decode(default_os_encoding),
                'pronunciation' : u'',
                'explain' : u''
            }
            result['pronunciation'], result['explain'] = online_dict[0].searchWord(result['word'])
            print result['pronunciation'].encode(default_os_encoding)
            print result['explain'].encode(default_os_encoding)
            results['bing'].append([result['word'], result['pronunciation'], result['explain']])


    except KeyboardInterrupt as e:
        pass


    print '\r\nsaving search results to dict.ods...',
    pyexcel_ods.write_data('dict.ods',results)
    print ('\r\n%d words saved!' % (len(results['bing'])))
