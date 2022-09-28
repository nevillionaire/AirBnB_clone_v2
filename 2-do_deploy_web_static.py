#!/usr/bin/python3
# distributes an archive to a web server.
from fabric.api import put
from fabric.api import run
import os.path
from fabric.api import env

env.hosts = ["ubuntu@18.206.194.154", "ubuntu@3.236.115.236"]


def do_deploy(archive_path):
    """Distributes an archive to a web server.
        Returns false If the file doesn't exist at
        archive_path or an error occurs
        Otherwise returns True.
    """
    if os.path.isfile(archive_path) is False:
        return False

    file_name_with_ext = archive_path.split("/")[-1]
    file_name_no_ext = file_name_with_ext.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file_name_with_ext)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(file_name_no_ext)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(file_name_no_ext)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file_name_with_ext, file_name_no_ext)).failed is True:
        return False
    if run("rm -r /tmp/{}".format(file_name_with_ext)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/"
           .format(file_name_no_ext, file_name_no_ext)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(file_name_no_ext)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(file_name_no_ext)).failed is True:
        return False
    print("New version deployed!")
    return True
