#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 部署所有组件：python devops.py deploy all
# 部署指定组件： python devops.py deploy ceilometer.yaml cinder.yaml
# 删除所有服务：python devops.py delete all
# 删除指定服务：python devops.py delete ceilometer.yaml cinder.yaml
# 替换所有镜像的registry或者tag：python devops.py replace all ,然后根据命令提示输入registry或者tag
# 替换指定镜像的registry或者tag: python devops.py replace cinder.yaml ceilometer.yaml ,然后根据命令提示输入registry或者tag


import os
import subprocess
import sys


options = ["deploy", "replace", "delete", "replace"]


# 获取所有模板文件
def show_all_yaml_files(direction=None):
    yaml_files = []
    if not direction:
        direction = os.getcwd()
    for f in os.listdir(direction):
        if f.endswith(".yaml"):
            yaml_files.append(f)
    return yaml_files


# 替换镜像的镜像仓库或者镜像tag
def replace(registry=None, tag=None, yamls=[]):
    yaml_to_be_modify = yamls
    if yamls:
        if yamls[0] == "all":
            yaml_to_be_modify = show_all_yaml_files()
        for ya in yaml_to_be_modify:
            with open(ya, 'r') as yaml:
                lines = yaml.readlines()
                with open(ya, 'w') as nya:
                    for line in lines:
                        if line.lstrip().startswith("image:"):
                            if registry:
                                line = line.split(":", 1)[0] + ": " + registry + "/" + \
                                       line.split(":", 1)[1].split("/")[
                                           1] + "\n"
                            if tag:
                                line = line.split("/", 1)[0] + "/" + line.split("/", 1)[1].split(":", 1)[
                                    0] + ":" + tag + "\n"
                            print line
                        nya.writelines(line)
    else:
        print "未提供需要修改的yaml文件"
        sys.exit()


# deploy openstack service to the k8s
def deploy(yamls=[]):
    if yamls:
        if yamls[0] == "all":
            print "部署所有yaml文件 "
            print show_all_yaml_files()
            res = subprocess.call("kubectl create -f ./", shell=True)
            if not res:
                print "部署成功！"
            else:
                print "请检查是否有yaml已经部署"
        else:
            print "部署如下yaml:"
            print yamls
            for y in yamls:
                res = subprocess.call("kubectl create -f ./%s" % y, shell=True)
                if res:
                    print "%s 部署失败" % y
                    continue
    else:
        print "错误操作!"


# delete openstack in the k8s
def delete(yamls=[]):
    if yamls:
        if yamls[0] == "all":
            res = subprocess.call("kubectl delete -f ./", shell=True)
        else:
            for y in yamls:
                res = subprocess.call("kubectl delete -f ./%s" % y, shell=True)


if __name__ == '__main__':
    option = None
    try:
        option = sys.argv[1]
    except IndexError, e:
        print "请提供一种操作"
        sys.exit()
    if option not in options:
        print "option:%s 未支持" % option
        sys.exit()
    else:
        if option == "deploy":
            deploy(sys.argv[2:])
        elif option == "replace":
            new_reg = None
            new_tag = None
            reg = raw_input("请输入新的registry(不更改registry请输入N):\n")
            if reg.lower() == "n":
                print "不更改registry"
            else:
                new_reg = reg
            ta = raw_input("请输入新的tag(不更改tag请输入N):\n")
            if ta.lower() == "n":
                print "不更改tag"
            else:
                new_tag = ta
            if new_reg or new_tag:
                replace(registry=new_reg, tag=new_tag, yamls=sys.argv[2:])
        elif option == "delete":
            delete(sys.argv[2:])
        else:
            pass