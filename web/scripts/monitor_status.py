# -*- coding:utf-8 -*-
"""
该文件主要用于读取系统状态.
"""

import time
import psutil
import logging
import signal
import sys

GBYTES = 1024 * 1024 * 1024
MBYTES = 1024 * 1024
level = logging.getLevelName("INFO")
logging.basicConfig(
    level=level,
    format="%(asctime)s [%(name)s] %(funcName)s[line:%(lineno)d] %(levelname)-7s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


class SystemStatusManager(object):

    @classmethod
    def read_cpu_usage(cls):
        info = psutil.cpu_percent(interval=5, percpu=False)
        logger.info(u"CPU使用百分比:{}".format(info * 100))

    @classmethod
    def read_mem_usage(cls):
        mem_filepath = '/proc/meminfo'
        mem_info = dict()
        with open(mem_filepath, 'r') as mem_file:
            for line in mem_file:
                if len(line) < 2:
                    continue
                name = line.split(':')[0]
                var = line.split(':')[1].split()[0]
                mem_info[name] = long(var) * 1024.0
        mem_info['MemUsed'] = mem_info['MemTotal'] - mem_info['MemFree'] - mem_info['Buffers'] - mem_info['Cached']
        total = int(mem_info['MemTotal'] / GBYTES)
        used = int(mem_info['MemUsed'] / MBYTES)
        free = int(mem_info['MemFree'] / MBYTES)
        buf = int(mem_info['Buffers'] / MBYTES)
        cache = int(mem_info['Cached'] / MBYTES)
        logger.info(u'总内存：{0}GB，使用内存：{1}MB，剩余内存：{2}MB, buffer内存：{3}MB，缓存内存：{4}MB'.format(total, used, free, buf, cache))

    @classmethod
    def get_sys_disk_info(cls):
        partition_info = psutil.disk_partitions()
        total = used = avail = 0
        for partition in partition_info:
            partition_total, partition_used, partition_avail = SystemStatusManager.get_disk_usage(partition.mountpoint)
            total += partition_total
            used += partition_used
            avail += partition_avail
        return total / GBYTES, used / GBYTES, avail / GBYTES

    @classmethod
    def get_disk_usage(cls, file_dir):
        dir_info = psutil.disk_usage(file_dir)
        return dir_info.total, dir_info.used, dir_info.free

    @classmethod
    def read_disk_usage(cls):
        database_total, database_used, database_avail = cls.get_sys_disk_info()
        logger.info(u'硬盘空间：{0}GB，使用空间：{1}GB，剩余空间：{2}GB'.format(
            database_total, database_used, database_avail))


def main(agrv):
    a = 0

    def signal_handle(dummy_signo, dummy_frame):
        logging.info('received a signal..................')
        global a
        a = 1
        logging.info(dummy_signo)
        logging.info(dummy_frame)
        time.sleep(5)
    signal.signal(signal.SIGUSR1, signal_handle)

    logger.info('=======monitor process start =======')
    while 1:
        SystemStatusManager.read_cpu_usage()
        SystemStatusManager.read_mem_usage()
        SystemStatusManager.read_disk_usage()
        logger.info('<<<=============================================================>>>\n')
        logging.info(a)
        time.sleep(60)


if __name__ == '__main__':
    main(sys.argv)
