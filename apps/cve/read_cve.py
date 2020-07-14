# -*- coding: utf-8 -*-
import xlrd
import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from apps.settings import DB_APT_URI
from apps.db.database import ANTAPT_Database
from apps.db.db import Cvelib


log = logging.getLogger(__name__)
apt_db = ANTAPT_Database(DB_APT_URI)
dbsession = apt_db.make_session()


def read_cve(cve_path):
    if not os.path.exists(cve_path):
        return None
    # 打开文件
    workbook = xlrd.open_workbook(cve_path)
    # 获取所有sheet
    sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(sheet_name)

    # 获取一行的内容
    column_dic = {'0': 'name',
                  '1': 'public_time',
                  '2': 'cve_id',
                  '3': 'cnnvd_id',
                  '4': 'bug_type',
                  '5': 'bug_level',
                  '6': 'cvss_scole',
                  '7': 'usability',
                  '8': 'bug_describe',
                  '9': 'solve_way',
                  '10': 'ref'
                  }

    # cve_list = []
    print(sheet.nrows)
    for i in range(1, sheet.nrows):
        cve = dict()
        for j in range(0, 11):
            if j == 6:
                cvss_scole = sheet.cell(i, j).value
                cve[column_dic.get(str(j))] = cvss_scole
                # print(cve[column_dic.get(str(j))])
                continue
            cve[column_dic.get(str(j))] = sheet.cell(i, j).value.encode('utf-8')
            # print(cve[column_dic.get(str(j))])

        cve['name'] = cve[column_dic.get(str(0))]
        cve['public_time'] = cve[column_dic.get(str(1))]
        cve['cve_id'] = cve[column_dic.get(str(2))]
        cve['cnnvd_id'] = cve[column_dic.get(str(3))]
        cve['bug_type'] = cve[column_dic.get(str(4))]
        cve['bug_level'] = cve[column_dic.get(str(5))]
        cve['cvss_scole'] = cve[column_dic.get(str(6))]
        cve['usability'] = cve[column_dic.get(str(7))]
        cve['bug_describe'] = cve[column_dic.get(str(8))]
        cve['solve_way'] = cve[column_dic.get(str(9))]
        cve['ref'] = cve[column_dic.get(str(10))]
        # cve_list.append(cve)
        try:
            # db.dbsession.execute(Cvelib.__table__.insert(), cve_list)
            dbsession.add(Cvelib(**cve))
            dbsession.commit()
            print(i)
        except SQLAlchemyError as e:
            log.error("Database error, adding cve_list: {0}".format(e))
            dbsession.rollback()
            return None, u'导入cve失败'
        except Exception as e:
            log.error("Error: {0}".format(e))
            return None, u'导入cve失败'
    # print('insert count: {}'.format(db.dbsession.query(Cvelib).count()))
    return None, u'保存cve漏洞库'


def main():
    logging.warn('<=====================开始导入CVE库=====================>')
    read_cve('./cve.xlsx')


if __name__ == "__main__":
    main()

