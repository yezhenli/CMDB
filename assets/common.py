#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@Time: 2017/2/14

@Author: Yezl
'''
def try_int(arg,default):
    '''
    整型转换
    '''
    try:
        arg = int(arg)
    except Exception,e:
        arg = default
    return arg