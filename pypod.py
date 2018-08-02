#!/usr/bin/env python
#-*- coding:utf-8 -*-

import httplib, urllib
import socket
import time
import sys
from datetime import datetime
import json

from config import *

params = dict(
    login_token=login_token,
    format="json",
    domain=domain,
    record_line='默认'
)

current_ip = None

def get_record_id(sub_domain):
    print('>> start get_record_id for {}...'.format(sub_domain))
    params.update(dict(sub_domain=sub_domain))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.List", urllib.urlencode(params), headers)

    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    data = json.loads(data)
    conn.close()
    if (len(data.get('records')) > 0):
        return data['records'][0]['id']
    else:
        return None
    

def update_record(ip, sub_domain, rid):
    print('>> start posting to dnspod...')
    params.update(dict(value=ip, sub_domain=sub_domain, record_id=rid))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)

    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
    return response.status == 200

def getip():
    print('>> start fetching public IP...')
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip

if __name__ == '__main__':
    while True:
        try:
            ip = getip()
            if current_ip != ip:
                print('IP changed @ {}: {}'.format(datetime.now(), ip))
                all_ok = True
                for sub in sub_list:
                    rid = get_record_id(sub)
                    if not rid:
                        print('!! cant get record_id for {}'.format(sub))
                        continue
                    print(rid)
                    if not update_record(ip, sub, rid):
                        all_ok = False
                if all_ok:
                    current_ip = ip
        except Exception, e:
            print('Exception happened: {}: {}'.format(datetime.now(), str(e)))
        sys.stdout.flush()
        time.sleep(60)