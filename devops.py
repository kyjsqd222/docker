#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys


options = ["deploy", "replace", "delete"]


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
def replace(registry=None, tag=None):
    for yamls in show_all_yaml_files():
        with open(yamls, 'r') as ya:
            lines = ya.readlines()
            with open(yamls, 'w') as nya:
                for line in lines:
                    if line.lstrip().startswith("image:"):
                        if registry:
                            line = line.split(":", 1)[0] + ": " + registry + "/" + line.split(":", 1)[1].split("/")[
                                1] + "\n"
                        if tag:
                            line = line.split("/", 1)[0] + "/" + line.split("/", 1)[1].split(":", 1)[
                                0] + ":" + tag + "\n"
                        print line
                    nya.writelines(line)


# deploy openstack service to the k8s
def deploy(yamls=[]):
    if yamls:
        if yamls[0] == "all":
            print "deploying all yamls "
            print show_all_yaml_files()
            res = subprocess.call("kubectl create -f ./", shell=True)
            if not res:
                print "all success"
            else:
                print "something wrong"
        else:
            print "deploying yamls below:"
            print yamls
            for y in yamls:
                res = subprocess.call("kubectl create -f ./%s" % y, shell=True)
                if res:
                    print "%s may be failed" % y
                    continue
    else:
        print "wrong options!"


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
        print "please supply right option"
        sys.exit()
    if option not in options:
        print "option:%s not supported yet" % option
        sys.exit()
    else:
        if option == "deploy":
            deploy(sys.argv[2:])
        elif option == "replace":
            pass
        elif option == "delete":
            delete(sys.argv[2:])
        else:
            pass