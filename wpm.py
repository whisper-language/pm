#!/usr/bin/env python

import getopt
import sys
import os
import configparser
import json
import requests
from pathlib import Path
import zipfile
import json
from zipfile import ZipFile
from os.path import basename
import shutil

version="0.1.0"
conf=configparser.ConfigParser()
home_ini=os.environ['WPM_HOME'];
print("WPM_HOME: "+home_ini);

def resolve_wpm_ini():   
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
    upload  						发布项目到当前仓库
	search <package_name>  			搜索指定依赖包
	install <package_name>  		安装指定依赖包
	uninstall <package_name> 		卸载指定依赖包
	tidy							清理无用的依赖
	run 							运行指定 wpn 脚本
	config get k 					获取指定配置
	config set k v		 			修改指定配置
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
            if res.headers['Content-Type']=='application/json':
                resData=json.loads(res.content)
                if resData['code']==-1:
                    print("ERROR:"+" "+ d +" version:"+dependencys[d]+" "+resData['msg']);
                return;
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

def zip(source,distFilename,zipObj):
        for folderName, subfolders, filenames in os.walk(source):
                for filename in filenames:
                    #create complete filepath of file in directory
                    if  filename=="vendor" or filename==distFilename :
                        continue
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    isFile = os.path.isfile(filePath)
                    if isFile==False:
                        print("xxx");
                    else:      
                        print("ADD "+filePath);
                        zipObj.write(filePath)  
def clean(arg):
    print("CLEAN "+"upload.zip");
    shutil.rmtree('./vendor');

def package(arg):
    with open('./wpm.json','r',encoding='utf8')as wpm_config:
        # 打包
        json_data = json.load(wpm_config)
        url=conf.get("default","publish_repo")+"/"+json_data['author']+"/"+json_data['name']+"/"+json_data["version"];
        print("PACKAGE "+"upload.zip");
        with ZipFile('upload.zip', 'w') as zipObj:
            zip(".","upload.zip",zipObj)

          
def upload(arg):
    with open('./wpm.json','r',encoding='utf8')as wpm_config:
        # 打包
        json_data = json.load(wpm_config)
        url=conf.get("default","publish_repo")+"/"+json_data['author']+"/"+json_data['name']+"/"+json_data["version"];
        file_size = os.stat("upload.zip")
        print("UPLOAD: "+url+" size:"+str(file_size.st_size))
        with open('upload.zip', 'rb') as f:
            files = {'file': f,"wpm.json":wpm_config}
            res=requests.post(url,files=files,data=json_data["publish"]);
            f.close();  
            resData=json.loads(res.content)
            if resData['code']==-1:
                print("ERROR:"+" "+ resData['msg']);
                return;
            else:
                print("SUCCESS");
            
            os.remove("upload.zip"); 
            
        
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
        opts, args=getopt.getopt(argv,'hiustr:c:v',["help","init","clean","package","update","search","install","upload","uninstall","tidy","run","config=","version"])
    except getopt.GetOptError:
        print("PARAMS PARSE ERROR")
        help()
    for opt, arg in opts:
        if opt in ("-h","--help"):
            help()
        elif opt in ("--init"):
            initproject()
        elif opt in ("-i","--install"):
            installDependency(arg)
        elif opt in ("-u","--upload"):
            package(arg);
            upload(arg)
        elif opt in ("-u","--clean"):
            clean(arg)
        elif opt in ("-p","--package"):
            package(arg)
        elif opt in ("-r","--run"):
            runscript(arg)
        elif opt in ("-v","--version"):
            print_version()
        elif opt in ("-c","--config"):              
            kv=arg.split("=")
            if len(kv)>1:
                print("SET:",arg)
                conf.set("default",kv[0],kv[1])
                with open(home_ini+"/wpm.ini", 'w') as configfile:
                    conf.write(configfile)
            else:
                print("参数:"+conf.get("default",kv[0]))
            pass
        else:
            print("未知的命令"+opt)

if __name__ =="__main__":
    resolve_wpm_ini();
    wpm_parse(sys.argv[1:])