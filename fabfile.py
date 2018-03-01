# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric.api import *

import os


fabfile_dir = os.path.dirname(__file__)
build_path = os.path.join(fabfile_dir, 'build')
image_name = 'moear'


@task
def build(ver='latest'):
    """镜像构建"""
    local('docker build -t littlemo/{name}:{ver} .'.format(
        name=image_name,
        ver=ver))


@task
def pack(ver='latest'):
    """镜像打包成.tar.gz"""
    if not os.path.exists(build_path):
        os.mkdir(build_path)
    arg_dict = {
        'ver': ver,
        'build': build_path,
        'name': image_name,
    }
    cmd_save = 'docker save littlemo/{name}:{ver} > ' + \
        'mo-{name}-{ver}.tar'
    with lcd(build_path):
        try:
            if os.path.exists('mo-{name}-{ver}.tar.gz'.format(**arg_dict)):
                local('rm mo-{name}-{ver}.ta*'.format(**arg_dict))
        except Exception:
            pass
        local('ls -alh')
        local(cmd_save.format(**arg_dict))
        local('tar czf mo-{name}-{ver}.tar.gz '
              'mo-{name}-{ver}.tar'.format(**arg_dict))
        local('ls -alh')
        local('rm mo-{name}-{ver}.tar'.format(**arg_dict))
