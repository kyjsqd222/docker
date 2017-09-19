#!/usr/bin/env python
# coding = utf-8

# need install docker : sudo pip install -U docker

import docker
import os
import subprocess
import sys


client = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto', timeout=10)
options_list = ["save", "delete", "load", "prune", "remove"]


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
        except OSError:
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


# delete all stopped containers
def prune_containers():
    client.containers.prune()


# delete all containers
def remove_containers():
    all_containers = client.containers.list(all=True)
    for c in all_containers:
        print c


if __name__ == '__main__':
    '''
    to save images: ./image_auto.py save [dire]
    to load images: ./image_auto.py load [dire]
    to delete images: ./image_auto.py delete 
    '''
    try:
        action = sys.argv[1]
        if action not in options_list:
            print "unsupported action!"
            sys.exit()
        else:
            if action == "save":
                try:
                    di = sys.argv[2]
                    save_images(dire=di)
                except IndexError:
                    save_images()
            elif action == "delete":
                delete_images()
            elif action == "load":
                try:
                    di = sys.argv[2]
                    load_images(di)
                except IndexError:
                    load_images()
            elif action == "prune":
                prune_containers()
            elif action == "remove":
                print "dangerous action!"
                remove_containers()
                pass
            else:
                print "waiting to add!"
    except IndexError:
        print "no action provided!"
        sys.exit()




