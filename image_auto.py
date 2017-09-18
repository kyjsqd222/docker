#!/usr/bin/env python

# need install docker : sudo pip install -U docker

import docker
import os
import subprocess
import sys


client = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto', timeout=10)


# save all docker images on the server
# def save_images(dire=None):
#    if not dire:
#        dire = "/home/my_images/"
#    try:
#        os.makedirs(dire)
#    except OSError, e:
#        pass
#    ima_list = []
#    for ima in client.images.list():
#        ima_list += ima.attrs.get("RepoTags")
#    for im in ima_list:
#        tar_name = im.encode("utf-8").split("/")[-1].split(":")[0]
#        image = client.images.get(im.encode("utf-8"))
#        resp = image.save()
#        f = open('%s%s.tar' % (dire, tar_name), 'w')
#        for chunk in resp.stream(decode_content=True):
#            f.write(chunk)
#        f.close()
#        break

def save_images(dire=None):
    if not dire:
        dire = "./"
    else:
        if not dire.endswith("/"):
            dire = dire+"/"
        try:
            os.makedirs(dire)
        except OSError, e:
            pass
    ima_list = []
    for ima in client.images.list():
        ima_list += ima.attrs.get("RepoTags")
    print ima_list
    for im in ima_list:
        tar_name = im.encode("utf-8").split("/")[-1].split(":")[0]
        print im, dire, tar_name
        cmd = "docker save %s > %s%s.tar" % (im, dire, tar_name)
        print "---------------------------"
        print cmd
        result = subprocess.call(cmd, shell=True)
        if not result:
            print "save %s successfully" % im
            print "---------------------------"


# load all docker images on the directions
def load_images(dire=None):
    if not dire:
        dire = "./"
    if not dire.endswith('/'):
        dire += "/"
    tar_list = os.listdir(dire)
    for im in tar_list:
        im = dire+im
        print im
        with open(im) as f:
            client.images.load(f)


# delete all images on the server
def delete_images():
    for ima in client.images.list():
        ima_id = ima.short_id.encode('utf-8').split(':')[-1]
        client.images.remove(ima_id)


if __name__ == '__main__':
    if sys.argv[1] == "save":
        if sys.argv[2]:
            save_images(sys.argv[2])
        else:
            save_images()
    elif sys.argv[1] == "load":
        if sys.argv[2]:
            load_images(sys.argv[2])
        else:
            load_images()
    elif sys.argv[1] == "delete":
        delete_images()
    else:
        print "options not suported"
        sys.exit()




