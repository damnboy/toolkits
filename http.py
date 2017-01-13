#!/usr/bin/env python
#coding=utf-8
import netaddr
from lxml import html
import config.dependency
from lib.http.methods import methods
from submodules.wfuzz.framework.ui.console.clparser import CLParser
from submodules.wfuzz.externals.reqresp.Request import Request
from lib.tasks.jobmanager import JobManager
from lib.tasks.queue import Job, OneoffJob
from lib.tasks.output import OutputFormatterConsole

class HTTPJob(OneoffJob):
    def __init__(self, id, req):
        OneoffJob.__init__(self, id)
        self._req = req
        self._description = req._Request__host

    def do(self):

        try:
            method = methods.transformer(self._req)
            response = method.make_request()
            if response._error != None:
                self._error = response._error
            else:
                self._result = dict.fromkeys(['body','header', 'code'])
                self._result['body'] = response._response_body
                self._result['header'] = response._response_header
                self._result['code'] = response._code
        except Exception as e:
            self._error = e

        finally:
            pass

        return OneoffJob.do(self)

class HTTPOutputFormatter(OutputFormatterConsole):
    def __init__(self):
        OutputFormatterConsole.__init__(self)

    def printResult(self, job):
        print '\r', job._description,
        if job._error != None:
            if isinstance(job._error, RuntimeError) == True:
                if job._error.message == 'read timeout':
                    print 'error: download page timeout'
            elif isinstance(job._error, UnicodeDecodeError) == True:
                print 'error: page decode error'
            else:
                print 'error: ', job._result['code']
        else:
            if len(job._result['body']) != 0:
                dom = html.fromstring(job._result['body'])
                node_title = dom.xpath('//title')
                if(len(node_title) != 0):
                    print node_title[0].text
            else:
                 print job._result['code']


class HTTPScanner(JobManager):
    def __init__(self):
        JobManager.__init__(self)
        self._outputFormatters.append(HTTPOutputFormatter())

    def createJobs(self, genTargets):
        for index, fuzzReq in enumerate(genReq):
            fuzzReq.setConnTimeout(5)
            self._jobQueue.addJob(HTTPJob(index, fuzzReq))


if __name__ == '__main__':
    cmd = 'reserve'
    subnet = netaddr.IPNetwork('198.177.122.6/24')
    subnet_first = netaddr.IPAddress(subnet.first)
    subnet_last = netaddr.IPAddress(subnet.last)
    for i in range(0,4):
        cmd = cmd + ' -z range,'
        cmd = cmd + str(subnet_first.words[i]) + '-' + str(subnet_last.words[i])

    #cmd = cmd + ' -z file,wordlist/general/common.txt'
    cmd = cmd + ' http://FUZZ.FUZ2Z.FUZ3Z.FUZ4Z'
    cmd = cmd.split(' ')
    options = CLParser(cmd).parse_cl()
    genReq = options.get("genreq")

    scanner = HTTPScanner()
    scanner.start(genReq, 16)

    for r in scanner:
        pass

