import sys
def Green(text):
    print("\033[1;32m%s\033[0m\n" %(text))


def Red(text):
    print("\033[1;31m%s\033[0m\n" %(text))


# 定义进度条函数
def progress_bar(domains, func,**kwargs):
    if func.__name__ == "assetfinderscan":
        func(domain_file=kwargs['domain_file'], alldomain=kwargs['alldomain'], platform=kwargs['platform'])

    else:
        for i in range(1,len(domains)+1):
            if func.__name__ =="fofascan":
                fofa_ip=func(domain=domains[i - 1],alldomain=kwargs['alldomain'])
                with open(kwargs['out_path'] + "/alive_ip.txt", 'w') as f:
                    f.write(fofa_ip)
            else:

                func(domain=domains[i-1],**kwargs)