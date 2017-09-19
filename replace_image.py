#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


# 获取所有模板文件
def list_files(direction=None):
    yaml_files = []
    if not direction:
        direction = os.getcwd()
    for f in os.listdir(direction):
        if f.endswith(".yaml"):
            yaml_files.append(f)
    return yaml_files

 
# 替换镜像的镜像仓库或者镜像tag
def replace(registry=None, tag=None):
    for yamls in list_files():
        with open(yamls, 'r') as ya:
            lines = ya.readlines()
            with open(yamls, 'w') as nya:
                for line in lines:
                    if line.lstrip().startswith("image:"):
                        if registry:
                            line = line.split(":", 1)[0]+": "+registry+"/"+line.split(":", 1)[1].split("/")[1]+"\n"
                        if tag:
                            line = line.split("/", 1)[0]+"/"+line.split("/", 1)[1].split(":", 1)[0]+":"+tag+"\n"
                        print line
                    nya.writelines(line)


if __name__ == '__main__':
    regis = None
    ta = None
    while True:
        registry_enable = raw_input("是否需要设置镜像仓库？y:是；n:否\n")
        if registry_enable.lower() == "y":
            regis = raw_input("请输入镜像仓库，形如：192.168.60.117:5000或者registry.com:5000:\n")
            confirm = raw_input("镜像仓库为：%s" % regis + " ,确认: y;重新设置：n\n")
            if confirm.lower() == "y":
                pass
            else:
                continue
        elif registry_enable.lower() == "n":
            print ("你选择了不设置镜像仓库")
            pass
        else:
            print ("输入错误")
            continue
        tag_enable = raw_input("是否需要设置镜像标签？y:是；n:否\n")
        if tag_enable.lower() == "y":
            ta = raw_input("请输入镜像标签:\n")
            confirm = raw_input("镜像标签为：%s" % ta + " ,确认: y;重新设置：n\n")
            if confirm.lower() == "y":
                break
            else:
                continue
        elif tag_enable.lower() == "n":
            print ("你选择了不设置镜像仓库")
            break
        else:
            print ("输入错误")
            continue
    if not regis and not ta:
        print ("****************************")
        print ("不对yaml文件做任何改变")
        pass
    else:
        replace(registry=regis, tag=ta)

