#!/usr/bin/env python

import getopt
import sys
import os
import configparser
import json
import requests
from pathlib import Path
import zipfile

version="0.1.0"
conf=configparser.ConfigParser()

def resolve_wpm_ini():
    home_ini=os.environ['WPM_HOME'];
    print("WPM_HOME: "+home_ini);
    if  os.path.exists(home_ini) :
        conf.read(home_ini+"/wpm.ini",encoding="utf-8")
    else:
       print("WPM_HOME 不存在")


def print_version():
    print("wpm version:"+version)
    
def help():
    print("""
    wpm  command <options>      
	init 							初始化一个项目
	update  						更新项目依赖
	search <package_name>  			搜索指定依赖包
	install <package_name>  		安装指定依赖包
	uninstall <package_name> 		卸载指定依赖包
	tidy							清理无用的依赖
	run 							运行指定 wpn 脚本
	config get k 						获取指定配置
	config set k v		 				修改指定配置
	help							打印帮助信息
	version							打印版本信息
    """)

def runscript(arg):
    with open('./wpm.json','r',encoding='utf8')as wpm_config:
        json_data = json.load(wpm_config)
        if arg in json_data["script"]:
            os.system(json_data["script"][arg])


def installDependency(arg):
    with open('./wpm.json','r',encoding='utf8')as wpm_config:
        json_data = json.load(wpm_config)
        dependencys=json_data["dependency"] 
        for d in dependencys:
            url=conf.get("default","global_repo")+"/"+d+"/"+dependencys[d];
            print("DOWNLOAD: "+url)
            res=requests.get(url)
            # 写入文件
            vender_path="./vendor/"+d+"/"+dependencys[d];
            Path(vender_path).mkdir(parents=True, exist_ok=True)
            tgzfile=vender_path+'/code.zip'
            with open(tgzfile,'wb') as fd:
                fd.write(res.content)
                fd.close()
                with zipfile.ZipFile(tgzfile) as zf:
                    zf.extractall(vender_path)
                    zf.close()
                    os.remove(tgzfile)                
        
def initproject():
    with open("./wpm.json", 'w') as wpm_config:
        wpm_config.write("""{
    "name":"name",
    "description":"",
    "license":"",
    "author":"username",
    "version":"0.1.0",
    "dependency":{
    },
    "script":{
        "test":"echo 'test'"
    }
}""")
        wpm_config.close()


def wpm_parse(argv):
    try:
        opts, args=getopt.getopt(argv,'hiustr:c:v',["help","init","update","search","install","uninstall","tidy","run","config=","version"])
    except getopt.GetOptError:
        print("参数解析错误")
        help()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            help()
        elif opt in ("--init"):
            initproject()
        elif opt in ("-i","--install"):
            installDependency(arg)
        elif opt in ("-r","--run"):
            runscript(arg)
        elif opt in ("-v","--version"):
            print_version()
        elif opt in ("-c","--config"):              
            kv=arg.split("=")
            if len(kv)>1:
                print("设置:",arg)
                conf.set("default",kv[0],kv[1])
                with open(globle_ini, 'w') as configfile:
                    conf.write(configfile)
            else:
                print("参数:"+conf.get("default",kv[0]))
            pass
        else:
            print("未知的命令"+opt)

if __name__ =="__main__":
    resolve_wpm_ini();
    wpm_parse(sys.argv[1:])