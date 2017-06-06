#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import re
import json
from subprocess import Popen, PIPE


class AnsibleAPI(object):
    def __init__(self, host, user, password):
        self.user= user
        self.password = password
        self.host = host

    def init(self):
        record = ("{ip} ansible_ssh_user={user} ansible_ssh_pass='{passwd}'".format(
                   ip     = self.host,
                   user   = self.user,
                   passwd = self.password
             ))
        with open('/etc/ansible/hosts', 'a') as f:
            print >>f, record

    def runcmd(self, ipl, cml):
        try:
            cmd = "ansible '{0}' -m shell -a '{1}'".format(ipl, cml)
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()
            if stdout:
                return stdout 
            elif stderr:
                return False, stderr
        except Exception, e:
            print e


    def getinfo(self, ip):
        try:
            cmd = "ansible '{0}' -m setup".format(ip)
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = proc.communicate()
            if stdout:
                res = stdout.split("=>")[1]
                ret = json.loads(res)
                deviceinfo = {}
                deviceinfo['hostname'] = ret['ansible_facts']['ansible_hostname']
                deviceinfo['address'] = ret['ansible_facts']['ansible_default_ipv4']['address']
                deviceinfo['interface'] = ret['ansible_facts']['ansible_default_ipv4']['interface']
                deviceinfo['gateway'] = ret['ansible_facts']['ansible_default_ipv4']['gateway']
                deviceinfo['macaddress'] = ret['ansible_facts']['ansible_default_ipv4']['macaddress']
                deviceinfo['cpu_cores'] = ret['ansible_facts']['ansible_processor_cores']
                deviceinfo['memory'] = ret['ansible_facts']['ansible_memtotal_mb']
                deviceinfo['disk'] = ret['ansible_facts']['ansible_mounts']
                deviceinfo['os'] = ret['ansible_facts']['ansible_lsb']['description']
                deviceinfo['kernel'] = ret['ansible_facts']['ansible_kernel']
                return deviceinfo
            elif stderr:
                return False, stderr
        except Exception, e:
            print e



def main():
    with open('/etc/ansible/hosts', 'w') as f:
        print >>f, '[qxb_server]'
    ipl = []
    for ip in ipl:
        ansb = AnsibleAPI(ip, 'root', '11111')
        ret = ansb.init()


if __name__ == '__main__':
    main()
    ansbapi = AnsibleAPI('qxb_server', 'demo', '11111')
    print ansbapi.runcmd('qxb_server', 'free -g')
