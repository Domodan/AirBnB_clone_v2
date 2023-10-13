#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers and deploy it
"""

from fabric.api import env, put, run, local
from os import path

env.hosts = ['100.25.201.83', '52.3.249.62']
env.user = 'ubuntu'
# env.key_filename = '<path_to_your_ssh_key>'


def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_root = archive_name.replace(".tgz", "")
    remote_path = "/tmp/{}".format(archive_name)

    # Upload archive to /tmp/ on web servers
    put(archive_path, remote_path)

    # Create folder for new version and uncompress the archive
    run("mkdir -p /data/web_static/releases/{}/".format(archive_root))
    run("tar -xzf {} -C /data/web_static/releases/{}/"
        .format(remote_path, archive_root))

    # Delete the archive
    run("rm {}".format(remote_path))

    # Delete the symbolic link current and create a new one
    current_path = "/data/web_static/current"
    run("rm -f {}".format(current_path))
    run("ln -s /data/web_static/releases/{}/ {}".format(archive_root))

    return True
