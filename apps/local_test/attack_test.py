# -*- coding:utf-8 -*-
import logging
from mails.models import Mails
from db.db_base import MTASDatabase
from settings import DB_APT_URI
from utils.ip_utils import GeoIP

geo = GeoIP()


class Attack_test(object):

    def __init__(self):
        self.internal_ip = ['222.82.232.162',  # 中国新疆
                            '27.224.243.35',  # 中国甘肃兰州
                            '1.25.36.14',  # 中国内蒙古自治区包头市
                            '42.101.192.15',  # 中国黑龙江省
                            '1.180.236.22',  # 中国山东省济南
                            '58.49.27.146',  # 中国湖北省
                            '14.204.84.114',  # 中国云南昆明
                            '59.50.33.23',  # 中国海南
                            '36.97.64.24',  # 中国浙江省
                            '61.234.42.33',  # 中国
                            '219.154.217.66',  # 中国河南将官池
                            '113.108.182.52',  # 中国广东广州
                            '119.39.23.134',  # 中国湖南长沙市
                            '220.243.255.22',  # 中国北京市
                            '36.152.45.25',  # 中国江苏省南京
                            '218.70.26.255',  # 中国上海 上海
                            '36.4.128.123',  # 中国安徽铜陵
                            '60.12.81.35',  # 中国浙江省
                            '59.62.82.8',  # 中国江西萍乡
                            '202.98.224.68'  # 中国西藏自治区
                            ]

        self.world_ip = ['101.119.255.255',  # 澳大利亚
                         '183.81.127.255',  # 越南
                         '152.255.255.255',  # 巴西
                         '105.187.255.255',  # 南非豪登省
                         '83.173.63.255',  # 冰岛
                         '103.242.99.255',  # 缅甸仰光
                         '219.122.241.181',  # 日本
                         '116.4.39.9',  # 中国广东
                         '176.215.255.255',  # 俄罗斯
                         '134.30.192.96',  # 德国
                         '152.255.255.255'  # 巴西
                         ]
        self.mtas_db = MTASDatabase(DB_APT_URI)
        self.session = self.mtas_db.make_session()

    def update_latest(self):
        try:
            mail_ids = self.session.query(Mails.id).filter(Mails.maltype.overlap('{1, 2, 3, 4, 5}')) \
                .order_by(Mails.access_time.desc()).limit(50).all()
            mail_ids = [mail[0] for mail in mail_ids]
            print mail_ids
            count = 0
            for id in mail_ids[:11]:
                mail = self.session.query(Mails).filter(Mails.id == id).first()
                logging.error(count)
                mail.sip = self.world_ip[count]
                mail.is_private_attack = False
                mail.is_national_attack = False
                mail.attack_address = u'{}{}{}'.format(*geo.city(mail.sip))
                self.session.merge(mail)
                self.session.commit()
                self.session.close()
                count = count + 1
            if len(mail_ids) > 11:
                count = 0
                for id in mail_ids[11:]:
                    mail = self.session.query(Mails).filter(Mails.id == id).first()
                    mail.sip = self.internal_ip[count]
                    mail.is_private_attack = False
                    mail.is_national_attack = True
                    mail.attack_address = u'{}{}{}'.format(*geo.city(mail.sip))
                    self.session.merge(mail)
                    self.session.commit()
                    self.session.close()
                    count = count + 1
        except Exception as err:
            self.session.rollback()
            logging.error('{}'.format(err))


def main():
    Attack_test().update_latest()


if __name__ == "__main__":
    main()
