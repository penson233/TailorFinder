# Tailorfinder

一款方便懒人对cn企业资产自动化收集工具,避免重复造轮子,因为将现有的信息工具缝起来并将结果自动进行去重并对fofa,hunter收集到的ip的c段进行统计,所以取名裁缝-Tailorfinder

收集的结果有子域名,c段,控股子公司，子公司及主公司主域名，邮箱,app资产

流程如下

![image-20230224225012311](https://cdn.jsdelivr.net/gh/penson233/images@main/uPic/image-20230224225012311.png)





结合以下信息收集工具




https://github.com/projectdiscovery/subfinder

https://github.com/tomnomnom/assetfinder

https://github.com/projectdiscovery/shuffledns

shuffledns 需要自行编译massdns

https://github.com/blechschmidt/massdns

已经为大家编译好了 开箱即用



以上工具自带，不需要自行编译安装





子域名收集api接口

fofa

hunter

securitytrails

rapiddns.io

crt.sh


邮箱查询网址
veryvp
hunter.io
www.email-format.com



使用前准备

shuffledns需要结合massdns使用请参考其github进行配置，二进制运行文件在bin目录下


配置config.py

准备fofo，hunter，SecurityTrails, hunteremailkey,爱奇查,天眼查 的key或者cookie



![image-20230224224444099](https://cdn.jsdelivr.net/gh/penson233/images@main/uPic/image-20230224224444099.png)





配置完成后

pip3 install -r requirements.txt

```
python3 main.py -h
```

![image-20230224224804192](https://cdn.jsdelivr.net/gh/penson233/images@main/uPic/image-20230224224804192.png)



```
python3.7 main.py -name 公司名称  -p 控股子公司的百分比 -o 输出路径
```



先收集主域名和子公司主域名

![image-20221207170002930](https://cdn.jsdelivr.net/gh/penson233/images@main/uPic/image-20221207170002930.png)



再利用以上信息工具进行收集子域名并输出为excel,总共有以下几个表格

![image-20230224224832989](https://cdn.jsdelivr.net/gh/penson233/images@main/uPic/image-20230224224832989.png)



如果大家有更好的工具或者api接口，欢迎联系g1itch_ctf@yahoo.com，我会放到裁缝里

