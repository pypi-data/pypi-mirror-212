#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
#############################################################
#                                                           #
#      Copyright @ 2023 -  Dashingsoft corp.                #
#      All rights reserved.                                 #
#                                                           #
#      Pyarmor                                              #
#                                                           #
#      Version: 8.0.1 -                                     #
#                                                           #
#############################################################
#
#
#  @File: pyarmor/runtime/__init__.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Mon Feb 13 09:17:27 CST 2023
#

#
# DEPRECATED Warning:
#
#   This package is not used since pyarmor 8.2.4
#
#   It's replaced by the following runtime packages:
#
#       - pyarmor.cli.core.windows
#       - pyarmor.cli.core.linux
#       - pyarmor.cli.core.darwin
#       - pyarmor.cli.core.alpine
#       - pyarmor.cli.core.freebsd
#       - pyarmor.cli.core.android
#       - pyarmor.cli.core.themida
#
#   Because it's too big to include all the runtime files for all the
#   platforms
#

import os
import zipfile

__VERSION__ = '3.2'


def map_platform(platname):
    if platname == 'darwin.aarch64':
        return 'darwin.arm64'
    return platname


class PyarmorRuntime(object):

    @staticmethod
    def get(platform, extra=None):
        platname = map_platform(platform)
        pkgpath = os.path.dirname(__file__)
        path = os.path.join(pkgpath, 'libs', platname, extra if extra else '')
        if os.path.exists(path):
            prefix = 'pyarmor_runtime'
            for entry in os.scandir(path):
                parts = entry.name.split('.')
                if parts[0] == prefix and parts[-1] in ('so', 'pyd', 'dylib'):
                    return entry.name, os.path.abspath(entry.path)

    def _get_from_zip(self, platform):
        path = __file__.replace('__init__.py', 'libs.zip')
        prefix = platform.replace('.', '_')
        with zipfile.ZipFile(path) as f:
            for name in f.namelist:
                if name.startswith(prefix):
                    return name[len(prefix)+1:], f.read(name)
