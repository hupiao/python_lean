# -*- coding:utf-8 -*-

import re
import os
import requests
import ConfigParser
import ipaddr
import logging
import urllib
import string
from pytz import timezone
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
# from apps.db.db import User, dbsession


# log = logging.getLogger(__name__)
#
# model_dict = {'user': User}

class Time_tools(object):

    @classmethod
    def current_utc8_time(cls):
        utc8_tz = timezone('Asia/Shanghai')
        return datetime.now(utc8_tz)

    @classmethod
    def generate_database_datetime_string(cls, time=None):
        time = time or cls.current_utc8_time()
        return time.strftime(time)

    @classmethod
    def get_last_24hour_time(cls):
        hourend = cls.current_utc8_time()
        hourstart = hourend - timedelta(days=1)
        return cls.generate_database_datetime_string(hourstart), cls.generate_database_datetime_string(hourend)

    @classmethod
    def get_last_week_time(cls):
        weekend = cls.current_utc8_time()
        weekstart = weekend - timedelta(days=7)
        return cls.generate_database_datetime_string(weekstart), cls.generate_database_datetime_string(weekend)

    @classmethod
    def gmt_to_datetime(cls, gmt, gmt_format='%b %d %H:%M:%S %Y GMT'):
        """
        convert GMT to datetime
        :param gmt: gmt string time
        :param gmt_format: gmt
        :return: datetime
        """
        dt = datetime.strptime(gmt, gmt_format)
        return dt


def is_ipv4_network(net_addr):
    try:
        ipaddr.IPv4Network(net_addr)
        return True
    except Exception as err:
        logging.warn("check ipv4 network address failed: %s" % err, exc_info=1)
        return False


def is_ipv6_network(net_addr):
    try:
        ipaddr.IPv6Network(net_addr)
        return True
    except Exception as err:
        logging.warn("check ipv4 network address failed: %s" % err, exc_info=1)
        return False


def search_escape(s):
    return re.sub(r"[(){}\[\].*?|^$\\+-]", r"\\\g<0>", s)


def bulk_insert_to_db(model, insert_list=[]):
    try:
        dbsession.execute(model_dict[model].__table__.insert(), insert_list)
        dbsession.commit()

        return insert_list, ''
    except SQLAlchemyError as e:
        log.error("Database error {0} adding ins: {1}".format(model, e))
        dbsession.rollback()
    except Exception as e:
        log.error("Error: {0}".format(e))
    return None, u'保存白名单失败'


class ConfigManager(object):
    """
    config manager
    """

    @classmethod
    def built_conf(cls, f):
        conf = ConfigParser.ConfigParser()
        conf.read(f)
        return conf

    def __init__(self, conf_path):
        self.conf_path = conf_path
        if not os.path.exists(self.conf_path):
            logging.error('Config {} not exists'.format(self.conf_path))
            raise Exception('not such file')
        self.bak_conf_path = '{}.bak'.format(self.conf_path)
        self.config = ConfigManager.built_conf(self.conf_path)

    def load_conf(self):
        result = {}
        for section in self.config.sections():
            result[section] = dict(self.config.items(section))

        return result

    def save_conf(self, section, data):
        try:
            for key, value in data.items():
                self.config.set(self, key, value)
            with open(self.conf_path, 'w') as f:
                self.config.write(f)
        except Exception as e:
            logging.error('Save config {} failure, errors{}'.format(self.conf_path, e))
            return False
        return True


# ===================Url 下载链接判断================= #

class Url_File_Download(object):

    @classmethod
    def is_downloadable(cls, url):
        """
        Does the url contain a downloadable resource
        """
        try:
            h = requests.head(url, allow_redirects=True, timeout=15)
            header = h.headers
            print(header)
            content_type = header.get('Content-type')
            if 'text' in content_type.lower():
                return False
            if 'html' in content_type.lower():
                return False
        except Exception as e:
            logging.error(e)
            return False
        return True

    @classmethod
    def get_filename_from_url(cls, url):
        """
        Get filename from content-disposition
        """
        try:
            r = requests.get(url, allow_redirects=True, timeout=15)
            if url.find('/'):
                return url.rsplit('/', 1)[1]
        except Exception as e:
            logging.error(e)
            return None
        return None

    @classmethod
    def _get_url_file_name(cls, url):
        """
        Get filename from the url contains download resource
        :param url: the url
        :return:
        """
        filename = url.rsplit('/', 1)[1]
        if not filename:
            return None
        return filename

    @classmethod
    def download_file(cls, url):
        """
        Download resource from the url contains a downloadable resource
        """
        try:
            r = requests.get(url, allow_redirects=True, timeout=15)
            filename = cls.get_filename_from_url(url)
            if filename:
                logging.warn('url filename: %s', filename)
                file_path = os.path.join("/tmp/", filename)
                open(file_path, 'wb').write(r.content)
                return file_path
        except Exception as e:
            logging.error(e)
            return None
        return None


if __name__ == "__main__":

    import  time
    # 时间格式为‘Tue, 08 May 2018 06:17:00 GMT’，现在想将它转换成‘2018-05-08 06:17:00’这种格式
    sample = 'Tue, 08 May 2018 06:17:00 GMT'
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

    sample_test = 'Sep 28 23:59:59 2019 GMT'
    GMT_FORMAT_TEST = '%b %d %H:%M:%S %Y GMT'
    d = datetime.strptime(sample_test,GMT_FORMAT_TEST)
    # print(type(d))

    # time_stamp = time.mktime(time.strptime("Sep 28 23:59:59 2019 GMT","%b %d %H:%M:%S %Y GMT"))
    # now_time_stamp = datetime.timestamp()
    # print(now_time_stamp > time_stamp)
    # timeStamp = 1381419600
    # timeArray = time.localtime(time_stamp)
    # print(type(timeArray))
    # print(time_stamp)
    end_time = datetime.strptime('Sep 28 23:59:59 2019 GMT', "%b %d %H:%M:%S %Y GMT")
    print(end_time)
    print(type(end_time))
    now_datetime = datetime.now()
    print(now_datetime)
    print(now_datetime>end_time)



    # s_t = datetime.strptime('2018-11-21 16:43:04', "%Y-%m-%d %H:%M:%S")
    # e_t = datetime.strptime('2018-11-23 00:43:04', "%Y-%m-%d %H:%M:%S")
    # print (e_t - s_t).seconds


    # print otherStyleTime  # 2013--10--10 23:40:00
    # 使用datetime

def init_log(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )