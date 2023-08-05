import datetime
from io import TextIOWrapper
import json
import os
import sys
from os.path import join,isfile,isdir,exists,isabs,dirname

def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)                 #没打包前的py目录

def readFile(path,content={}):
    if '.json' in path:
        if not os.path.exists(path):
            with open(path,'w',encoding='utf-8') as fp:
                json.dump(content,fp,ensure_ascii=False)
        with open(path,'r',encoding='utf-8') as fp:
            content = json.loads(fp.read())
    else:
        if not os.path.exists(path):
            with open(path,'w',encoding='utf-8') as fp:
                fp.write('{}'.format(content))
        with open(path,'r',encoding='utf-8') as fp:
            content = fp.read()
    return content

def getLength(text):
    return len(text)
def read_files_write(fw:TextIOWrapper,relative_path=''):
    path=join(basedir,relative_path)
    # print(path)
    if isfile(path):
        configDict["text"]+=relative_path+'\n'
        try:
            with open(path,'r',encoding='utf-8') as fp:
                configDict["text"]+=fp.read()
        except UnicodeDecodeError as res:
            print(res)
            print("{}非文本文件，已自动跳过".format(relative_path))
        configDict["text"]+='\n\n'
        if getLength(configDict["text"])>length:
            fw.write(configDict["text"])
            configDict["text"]=''
    else:
        for filename in os.listdir(path):
            
            read_files_write(fw,join(relative_path,filename))
def dir_exist(path:str,op=1):
    if not os.path.exists(path):
        if op==1:
            os.makedirs(path)
        return False
    else:
        return True
    
def check_target_path(target_path,filetype='.txt'):
    if not isabs(target_path):
        print("生成目录非绝对路径,请重新配置")
        1/0
    if '.' in target_path:
        if not exists(dirname(target_path)):
            print("生成目录不存在请重新配置")
            1/0
    else:
        if not exists(target_path):
            print("生成目录不存在请自行配置")
            1/0
    if isdir(target_path):
        filename=str(datetime.datetime.now()).replace(":",'-')+filetype
        target_path=join(target_path,filename)
    else:
        if target_path[-4:]!=filetype:
            target_path+=filetype
    return target_path
if __name__=='__main__':
    configPath=app_path()+'/config.json'
    target_path=app_path()+"/结果"
    configDict={"basedir":"","target_path":target_path,"length":1024,"input_type":0,"text":""}
    if not dir_exist(target_path):
        print("结果目录不存在，已自动生成")
    configDict=readFile(configPath,configDict)
    input_type=configDict["input_type"]
    
    try:
        while True:
            with open(configPath,"r",encoding="utf-8") as fp:
                configDict=json.loads(fp.read())
            length=configDict["length"]
            text=configDict["text"]
            target_path=configDict["target_path"]
            input_type=configDict["input_type"]
            if input_type==0:
                basedir=configDict["basedir"]
            else:
                basedir=input("读取目录:")
            
            target_path=check_target_path(target_path)
            if basedir=="":
                basedir=input("读取目录:")
                # if input("检测到读取目录配置为空,是否想要遍历程序所存放的当前目录,是输入1,否输入其他:")=='1':
                #     pass
                # else:
                #     pass
            if isabs(basedir) and exists(basedir):
                with open(target_path,'w',encoding='utf-8') as fp:
                    fp.write('')
                with open(target_path,'a',encoding='utf-8') as fw:
                    read_files_write(fw)
            else:
                # input_type=input("检测到非绝对路径,或者文件不存在,请输入任意非0数字继续:")
                print(("检测到非绝对路径,或者文件不存在"))
                input_type=1
            input("请输入任意数字继续:")

    except ZeroDivisionError as res:
        # print(res)
        pass
    except Exception as res:
        print(res)
    print("程序已结束，请检查操作...")