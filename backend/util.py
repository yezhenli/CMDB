#!/usr/bin/env python
#coding:utf-8
import os,sys
import logging,logging.config


def write_log(logger_name):
    work_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_conf = os.path.join(work_dir,'conf/logger.conf')
    logging.config.fileConfig(log_conf)
    logger = logging.getLogger(logger_name)
    return logger
