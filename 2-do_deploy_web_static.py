#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import local
from datetime import datetime
from os.path import isfile
from fabric.api import *

env.user = 'ubuntu'
env.hosts = ['100.25.201.83', '52.3.249.62']


def do_pack():
    """ Generate a .tgz archive from the contents of the web_static folder """
    time = datetime.now()
    name = 'web_static_' + str(time.year) + str(time.month) + str(time.day)
    name = name + str(time.hour) + str(time.minute) + str(time.second) + '.tgz'
    local('sudo mkdir -p versions')
    archive = local('tar -cvzf versions/{} web_static'.format(name))
    if archive.failed:
        return None
    return 'versions/{}'.format(name)


def do_deploy(archive_path):
    """ Distribute an archive to the web servers """
    if not isfile(archive_path):
        return False
    put(archive_path, '/tmp/')
    archive = archive_path.replace('.tgz', '')
    archive = archive.replace('versions/', '')
    run('sudo mkdir -p /data/web_static/releases/{}/'.format(archive))
    run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
        .format(archive, archive))
    run('sudo rm /tmp/{}.tgz'.format(archive))
    run('sudo mv /data/web_static/releases/{}/web_static/* '.format(archive) +
        '/data/web_static/releases/{}/'.format(archive))
    run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(archive))
    run('sudo rm -rf /data/web_static/current')
    run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
        .format(archive))
    print('New version deployed!')
    return True
