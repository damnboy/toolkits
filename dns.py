#!/usr/bin/env python
#coding=utf-8

import random
import socket
import config.dependency
from submodules.subbrute.subbrute import *

#https://zh.wikipedia.org/wiki/%E6%A0%B9%E7%B6%B2%E5%9F%9F%E5%90%8D%E7%A8%B1%E4%BC%BA%E6%9C%8D%E5%99%A8
top_level_nameservers = {
    'A' :   ['198.41.0.4']         #VeriSign
    ,'B':    ['192.228.79.201']
    ,'C':    ['192.33.4.12']
    ,'D':    ['199.7.91.13']
    ,'E':    ['192.203.230.10']
    ,'F':    ['192.5.5.241']
    ,'G':    ['192.112.36.4']
    ,'H':    ['198.7.190.53']
    ,'I':    ['192.36.148.17']
    ,'J':    ['192.58.128.30']
    ,'K':    ['193.0.14.129']
    #,'L' :   ['199.7.83.42']
    #,'M' :   ['202.12.27.33']
}
class domain_resolver :
    def __init__(self, domain, name_servers = top_level_nameservers):
        self.domain = domain
        self.info = {
            'ns' : name_servers,
            'mx' : {}
        }

    def extract_ns_records(self, response):
        new_ns_server = {}
        if response:
            rcode = dnslib.RCODE[response.header.rcode]

            #response中的ar记录包含ns服务器的ip地址
            for auth in response.auth:
               new_ns_server[str(auth.rdata).rstrip(".")] = []

            #response中的aa记录包含ns服务器的FQDN
            for ar in response.ar:
                try:
                    rtype = str(dnslib.QTYPE[ar.rtype])
                except:#Server sent an unknown type:
                    rtype = str(ar.rtype)

                #Fully qualified domains may cause problems for other tools that use subbrute's output.
                rhost = str(ar.rname).rstrip(".")

                if rtype in ['A']: #重置self.ns_servers
                    if new_ns_server.get(rhost) == None:
                        new_ns_server[rhost] = []
                    new_ns_server[rhost].append(str(ar.rdata))

        return new_ns_server

    def get_random_ns(self):
        ns_servers = []
        for k, v in self.info['ns'].items():
            ns_servers.extend(v)
        index = random.randint(0 , len(ns_servers)-1)
        return ns_servers[index]

    def get_a(self, qfdn):
        records = []
        query = dnslib.DNSRecord.question(qfdn, 'A'.upper().strip())
        try:
            ns = self.get_random_ns()
            print '正在尝试从 %s 上获取 %s 所在的ip地址信息 ' % (ns , qfdn)
            response_q = query.send(ns, 53, False)
            if response_q:
                response = dnslib.DNSRecord.parse(response_q)
            else:
                raise IOError("Empty Response")
        except Exception as e:
            #IOErrors are all conditions that require a retry.
            raise IOError(str(e))

        if response:
            rcode = dnslib.RCODE[response.header.rcode]
            if len(response.rr) == 0:
                self.info['ns'] = self.extract_ns_records(response)
                return self.get_a(qfdn)

            else:
                for rr in response.rr:
                    records.append(str(rr.rdata))

        return records;

    def get_domain_mx(self):
        query = dnslib.DNSRecord.question(self.domain, 'MX'.upper().strip())
        try:
            ns = self.get_random_ns()
            response_q = query.send(ns, 53, False)
            if response_q:
                response = dnslib.DNSRecord.parse(response_q)
            else:
                raise IOError("Empty Response")
        except Exception as e:
            #IOErrors are all conditions that require a retry.
            raise IOError(str(e))

        if response:
            rcode = dnslib.RCODE[response.header.rcode]
            for rr in response.rr:
                try:
                    rtype = str(dnslib.QTYPE[rr.rtype])
                except:#Server sent an unknown type:
                    rtype = str(rr.rtype)

                #Fully qualified domains may cause problems for other tools that use subbrute's output.
                rhost = str(rr.rdata.label).rstrip(".")

                if rtype in ['MX']:
                    self.info['mx'][rhost] = []

            #for mx in self.info['mx'].keys():
            #    self.info['mx'][mx].extend(self.get_a(mx))
            #    print self.info['mx'][mx]

        return self.info['mx']

    def get_domain_ns(self):
        levels = self.domain.split('.')
        for i in range(len(levels) -1 , -1 , -1):
            domain = '.'.join(levels[i : len(levels)])
            query = dnslib.DNSRecord.question(domain, 'NS'.upper().strip())
            try:
                ns = self.get_random_ns()
                response_q = query.send(ns, 53, False)
                if response_q:
                    response = dnslib.DNSRecord.parse(response_q)
                else:
                    raise IOError("Empty Response")
            except Exception as e:
                #IOErrors are all conditions that require a retry.
                raise IOError(str(e))

            if response:
                rcode = dnslib.RCODE[response.header.rcode]
                self.info['ns'] = self.extract_ns_records(response)
                print '通过 %s 获取到 %d 个 %s 的权威域名服务器' %(ns, len(self.info['ns']), domain)

        return self.info['ns']

    def test_zone_transfer(self):
        ns_servers = []
        for k, v in self.info['ns'].items():
            ns_servers.extend(v)

        for ns_server in ns_servers:
            query = dnslib.DNSRecord.question(domain, 'AXFR'.upper().strip())
            try:
                response_q = query.send(ns_server, 53, False)
                if response_q:
                    response = dnslib.DNSRecord.parse(response_q)
                else:
                    raise IOError("Empty Response")
            except Exception as e:
                #IOErrors are all conditions that require a retry.
                raise IOError(str(e))

            if response:
                rcode = dnslib.RCODE[response.header.rcode]
                print ns_server, 'zone transfer ', rcode


if __name__ == '__main__':
    domain = 'qq.com'
    r = domain_resolver(domain)
    ns_records =  r.get_domain_ns()
    print '在域名 %s 上检测到 %d 条NS记录' % (domain, len(ns_records))
    for k,v in ns_records.items():
        print k, v

    mx_records =  r.get_domain_mx()
    print '在域名 %s 上检测到 %d 条MX记录' % (domain, len(mx_records))
    for k,v in mx_records.items():
        print k, v


    r.test_zone_transfer()














