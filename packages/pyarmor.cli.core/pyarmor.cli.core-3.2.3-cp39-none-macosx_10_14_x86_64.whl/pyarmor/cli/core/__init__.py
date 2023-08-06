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
#  @File: pyarmor/core/__init__.py
#
#  @Author: Jondy Zhao (pyarmor@163.com)
#
#  @Create Date: Thu Jan 12 17:29:25 CST 2023
#

__VERSION__ = '3.2'

# Each log
#    revision, age, (new features), (changed features), (removed features)
__CHANGE_LOGS__ = (
    (1, 0, (), (), ()),
)


def format_platform():
    import platform
    import sys
    from struct import calcsize

    def format_system():
        plat = platform.system().lower()
        plat = ('windows' if plat.startswith('cygwin') else
                'linux' if plat.startswith('linux') else
                'freebsd' if plat.startswith(
                    ('freebsd', 'openbsd', 'isilon onefs')) else plat)
        if plat == 'linux':
            if hasattr(sys, 'getandroidapilevel'):
                plat = 'android'
            else:
                cname, cver = platform.libc_ver()
                if cname == 'musl':
                    plat = 'alpine'
                elif cname == 'libc':
                    plat = 'android'
        return plat

    def format_machine():
        mach = platform.machine().lower()
        arch_table = (
            ('x86', ('i386', 'i486', 'i586', 'i686')),
            ('x86_64', ('x64', 'x86_64', 'amd64', 'intel')),
            ('arm', ('armv5',)),
            ('armv6', ('armv6l',)),
            ('armv7', ('armv7l',)),
            ('aarch32', ('aarch32',)),
            ('aarch64', ('aarch64', 'arm64'))
        )
        for alias, archlist in arch_table:
            if mach in archlist:
                mach = alias
                break
        return mach

    plat, mach = format_system(), format_machine()
    if plat == 'windows' and mach == 'x86_64':
        bitness = calcsize('P'.encode()) * 8
        if bitness == 32:
            mach = 'x86'
    return plat, mach


def _import_pytransform3():
    try:
        return __import__(
            'pytransform3', globals=globals(), locals=locals(),
            fromlist=('__pyarmor__',), level=1
        )
    except ModuleNotFoundError:
        modname = '.'.join(format_platform() + ('pytransform3',))
        return __import__(
            modname, globals=globals(), locals=locals(),
            fromlist=('__pyarmor__',), level=1
        )


class Pytransform3(object):

    _pytransform3 = None

    @staticmethod
    def init(ctx=None):
        if Pytransform3._pytransform3 is None:
            Pytransform3._pytransform3 = m = _import_pytransform3()
            if ctx:
                m.init_ctx(ctx)
        return Pytransform3._pytransform3

    @staticmethod
    def generate_obfuscated_script(ctx, res):
        m = Pytransform3.init(ctx)
        return m.generate_obfuscated_script(ctx, res)

    @staticmethod
    def generate_runtime_package(ctx, output, platforms=None):
        m = Pytransform3.init(ctx)
        return m.generate_runtime_package(ctx, output, platforms)

    @staticmethod
    def generate_runtime_key(ctx, outer=None):
        m = Pytransform3.init(ctx)
        return m.generate_runtime_key(ctx, outer)

    @staticmethod
    def pre_build(ctx):
        m = Pytransform3.init(ctx)
        return m.pre_build(ctx)

    @staticmethod
    def post_build(ctx):
        m = Pytransform3.init(ctx)
        return m.post_build(ctx)

    @staticmethod
    def _update_token(ctx):
        m = Pytransform3.init(ctx)
        m.init_ctx(ctx)

    @staticmethod
    def get_hd_info(hdtype, name=None):
        m = Pytransform3.init()
        return m.get_hd_info(hdtype, name) if name \
            else m.get_hd_info(hdtype)

    @staticmethod
    def version():
        m = Pytransform3.init()
        return m.revision


class PyarmorRuntime(object):

    @staticmethod
    def get(plat=None, extra=None):
        from os import listdir, path as os_path
        prefix = 'pyarmor_runtime'

        path = __file__.replace('__init__.py', '')
        for x in listdir(path):
            if x.startswith(prefix) and x[-3:] in ('.so', 'pyd'):
                if extra is None or extra in x.split('.'):
                    return x, os_path.join(path, x)

        path = os_path.join(path, *plat.split('.'))
        for x in listdir(path):
            if x.startswith(prefix) and x[-3:] in ('.so', 'pyd'):
                if extra is None or extra in x.split('.'):
                    return x, os_path.join(path, x)


class PyarmorFeature(object):

    def features(self):
        '''return features list from change logs'''
        result = set()
        [result.update(item[2]) for item in __CHANGE_LOGS__]
        return result

    def life(self, feature):
        '''return first pyarmor_runtime version and last verstion to support
        this feature.'''
        minor, fin = None
        for item in __CHANGE_LOGS__:
            if feature in item[2] + item[3]:
                minor = item[0]
            if feature in item[-1]:
                fin = item[0]
        return minor, fin
