#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys
import subprocess


version_content = """version_name = '{name}'
version_code = '{code}'
"""

# 获取版本名
cmd_version_name = 'git describe --tags'
out, err = subprocess.Popen(
    cmd_version_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    shell=True).communicate()
if len(err) != 0:
    print('获取<版本名>失败: {}'.format(err))
    sys.exit(1)
version_name = out.decode().strip()

# 获取版本号
cmd_version_name = "git rev-list HEAD | wc -l | awk '{print $1}'"
out, err = subprocess.Popen(
    cmd_version_name, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    shell=True).communicate()
if len(err) != 0:
    print('获取<版本号>失败: {}'.format(err))
    sys.exit(1)
version_code = out.decode().strip()

# 生成version.py文件
print('> Current Soft VersionName is [{name}], VersionCode is [{code}]'.format(
    name=version_name,
    code=version_code))
with open('server/server/config/version.py', 'w') as f:
    f.write(version_content.format(
        name=version_name,
        code=version_code))
    print('> Update version.py ... finish!')
