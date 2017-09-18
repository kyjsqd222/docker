#!/usr/bin/env python

# need install docker : sudo pip install -U docker

import docker
import os

client = docker.DockerClient(base_url='unix://var/run/docker.sock', version='auto', timeout=10)


# save all docker images on the server
def save_images(dire=None):
    if not dire:
        dire = "/home/my_images/"
    try:
        os.makedirs(dire)
    except OSError, e:
        pass
    ima_list = []
    for ima in client.images.list():
        ima_list += ima.attrs.get("RepoTags")
    for im in ima_list:
        tar_name = im.encode("utf-8").split("/")[-1].split(":")[0]
        image = client.images.get(im)
        resp = client.images.model.save(image)
        f = open('%s%s.tar' % (dire, tar_name), 'w')
        for chunk in resp.stream():
            f.write(chunk)
        f.close()
        break


# load all docker images on the directions
def load_images(dire=None):
    if not dire:
        dire = "./"
    if not dire.endswith('/'):
        dire += "/"
    tar_list = os.listdir(dire)
    for im in tar_list:
        im=dire+im
        print im
        with open(im) as f:
            client.images.load(f)


# delete all images on the server
def delete_images():
    for ima in client.images.list():
        ima_id = ima.short_id.encode('utf-8').split(':')[-1]
        client.images.remove(ima_id)


if __name__ == '__main__':
    delete_images()
    load_images('/home/jx')
    save_images("/home/jx/")

