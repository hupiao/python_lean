# -*-coding:utf-8-*-

import os
import struct
import hashlib
import zmq
import time
import sys
import proto
import threading
import getopt

from sensor_log_pb2 import SENSOR_LOG


class SendFile(threading.Thread):
    def __init__(self, name, host, port, file_path, send_interval, debug=0):
        threading.Thread.__init__(self)
        self.thread_name = name
        self.daemon = False
        self.HOST = host
        self.PORT = port
        self.FILE_DIR = file_path
        self.SEND_INTERVAL = send_interval * 0.001
        self.URL = "tcp://%s:%d" % (self.HOST, int(self.PORT))
        self.DEBUG = 0
        self.total_files = 0
        self.file_list = []
        self.speed = 0
        self.send_num = 0

    def get_file_list(self, dir="."):
        filelist = []
        if os.path.isfile(self.FILE_DIR):
            filelist.append(self.FILE_DIR)
            return filelist

        if not os.path.samefile(os.getcwd(), self.FILE_DIR):
            os.chdir(self.FILE_DIR)

        for file_name in os.listdir(dir):
            path = os.path.join(dir, file_name)
            if os.path.isdir(path):
                filelist += self.get_file_list(path)
            else:
                filelist.append(file_name)
        return filelist

    def get_files_list_list(self):
        self.file_list = self.get_file_list()
        self.total_files = len(self.file_list)
        print "%s Load total %s files" % (self.thread_name, self.total_files)

    def get_log_entry(self, md5, content_type):
        type, LOG_ENTRY = proto.logety()
        result = SENSOR_LOG()

        if type == 'mail':
            result.message_type = 14
            file_log = result.skyeye_mail_sandbox
            file_log.attach_md5 = md5
        else:
            result.message_type = 7
            file_log = result.skyeye_file_sandbox
            file_log.file_md5 = md5

        file_log.serial_num = "1000101201406003"
        for items in LOG_ENTRY.split('\x07'):
            key, value = items.split(':', 1)
            if key in ["sport", "dport"]:
                value = int(value)
            setattr(file_log, key, value)

        file_log.mime_type = content_type
        return result.SerializeToString()

    def get_data_buff(self, content):
        md5 = hashlib.md5(content).hexdigest()
        content_type = "text/html"
        type_len = len(content_type)
        log_entry = self.get_log_entry(md5, content_type)
        log_len = len(log_entry)
        content_len = len(content)
        format_string = "<2b%dsH%dsH%dsi%ds" % (len(md5), type_len, log_len, content_len)
        data_buff = struct.pack(format_string, 2, 0, md5, type_len, content_type, log_len, log_entry, content_len,
                                content)

        if self.DEBUG:
            print "md5: %s len: %d" % (md5, len(data_buff))

        return (data_buff, md5)

    def get_content(self, filename):
        with open(filename, 'rb') as read_file:
            return read_file.read()

    def get_percent(self, d1, d2):
        return float(d1) / d2 * 100

    def send_file(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)
        socket.connect(self.URL)
        data = {}

        for file_name in self.file_list:
            data_buff, md5 = self.get_data_buff(self.get_content(os.path.join(self.FILE_DIR, file_name)))
            data[md5] = data_buff

        t1 = time.time()
        for m in data.keys():
            socket.send(data[m])
            self.send_num += 1
            time.sleep(self.SEND_INTERVAL)
        t2 = time.time()
        del data
        socket.close()

        print t1, t2
        self.speed = int(self.total_files / (t2 - t1))
        print "%s:send total %s files in %s seconds, %s files per second" % (
            self.thread_name, self.total_files, (t2 - t1), self.speed)

    def run(self):
        self.get_files_list_list()
        self.send_file()


def usage():
    print 'usage:'
    print '-h,--help:print help message'
    print '-H,--host:sandbox host ip,default 10.16.66.29'
    print '-p,--port:sandbox port,default 6666'
    print '-n,--pnum:process number,default 1'
    print '-s,--send:send time interval,default 20ms'
    print '-d,--dir:file dir'
    print '-l,--log:log file dir'
    print 'example: python2.7 sendfile.py -H 192.168.1.29 -p 6666 -n 1 -s 1 -d /home/temp/static/ -l /tmp/speed'


def getopts(argvs):
    HOST = '192.168.1.29'
    PORT = 6666
    FILE_DIR = '/home/temp/static/'
    PNUM = 1
    SEND_INTERVAL = 1
    LOG_FILE = '/tmp/speed'

    try:
        opts, args = getopt.getopt(argvs, "hH:p:n:s:d:l:",
                                   ["help", "host=", "port=", "pnum=", "send=", "dir=", "--log="])
        # print opts

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit(1)
            elif opt in ("-H", "--host"):
                HOST = arg
            elif opt in ("-p", "--port"):
                PORT = int(arg)
            elif opt in ("-n", "--pnum"):
                PNUM = int(arg)
            elif opt in ("-s", "--send"):
                SEND_INTERVAL = int(arg)
            elif opt in ("-d", "--dir"):
                FILE_DIR = arg
            elif opt in ("-l", "--log"):
                LOG_FILE = arg
            else:
                print "Invalid parameters"
                usage()
                sys.exit(1)

        return HOST, PORT, FILE_DIR, PNUM, SEND_INTERVAL, LOG_FILE
    except getopt.GetoptError:
        usage()
        sys.exit(1)


# python2  sendfile.py  -H  10.91.3.16  -p  6666  -n  1  -s  1  -d ./samples/
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    host, port, file_dir, pnum, send_interval, log_file = getopts(sys.argv[1:])

    print file_dir
    file_dir = os.path.abspath(file_dir)
    print file_dir

    th = []
    for x in xrange(pnum):
        th.append(SendFile('Thread-' + str(x), host, port, file_dir, send_interval))

    for p in th:
        p.start()

    for p in th:
        p.join()

    speed = 0
    for p in th:
        print p.speed
        speed += p.speed

    print "Stop Run, Send speed: %s" % speed

    with open(log_file, 'w') as f:
        f.write(str(speed))

__author__ = 'wen'
