#!/usr/bin/env python
# coding = utf-8

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
    for im in ima_list:
        tar_name = im.encode("utf-8").split("/")[-1].split(":")[0]
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
        if not im.endswith(".tar"):
            continue
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
    '''
    to save images: ./image_auto.py save [dire]
    to load images: ./image_auto.py load [dire]
    to delete images: ./image_auto.py delete 
    '''
    try:
        if sys.argv[1] == "save":
            try:
                save_images(sys.argv[2])
            except IndexError, e:
                print "save in the current file"
                save_images()
    except IndexError, e:
        sys.exit()
    try:
        if sys.argv[1] == "load":
            try:
                load_images(sys.argv[2])
            except IndexError, e:
                load_images()
    except IndexError, e:
        sys.exit()
    try:
        if sys.argv[1] == "delete":
            delete_images()
        if sys.argv[1] not in ["save", "load", "delete"]:
            print "options not supported yet!"
    except IndexError, e:
        print "options not supplied!"
        sys.exit()




