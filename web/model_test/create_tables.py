# -*-coding: utf-8 -*-
import logging
from antapt import AntaptDatabase


def create_table():
    logging.info("=============================")
    db = AntaptDatabase(pool_size=50)
    db.create_tables()  # 父类Base调用所有继承他的子类来创建表结构


if __name__ == "__main__":
    logging.info("dddddddddddddddddd")
    create_table()
