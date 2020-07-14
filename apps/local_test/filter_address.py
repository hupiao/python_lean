# -*- coding:utf-8 -*-
import logging
import xlrd
import os
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def read_cve(cve_path):
    try:
        if not os.path.exists(cve_path):
            print "========================"
            return None
        # 打开文件
        workbook = xlrd.open_workbook(cve_path)
        # 获取所有sheet
        sheet_name = workbook.sheet_names()[0]
        sheet = workbook.sheet_by_name(sheet_name)

        tmp_list = []
        print(sheet.nrows)
        for i in range(1, sheet.nrows):
            addr = dict()
            addr['country'] = sheet.cell(i, 0).value.encode('utf-8')
            addr['province'] = sheet.cell(i, 1).value.encode('utf-8')
            addr['city'] = sheet.cell(i, 2).value.encode('utf-8')
            addr['county'] = sheet.cell(i, 3).value.encode('utf-8')
            addr['longitude'] = sheet.cell(i, 4).value
            addr['latitude'] = sheet.cell(i, 5).value
            if addr['city'] == addr['county']:
                print addr['province'], addr['city'], addr['county']
                tmp_list.append(addr)
        # tmp_list.insert(0, {'country': u'国家', 'province': u'省份', 'city': u'地市', 'county': u'区县',
        # 'longitude': u'经度', 'latitude': u'纬度' })
        workbook = xlsxwriter.Workbook('./tmp.xlsx')
        # 添加工作区
        sheet = workbook.add_worksheet("Sheet1")
        sheet.set_column("A:A", 40)  # 设置列宽度
        # bold_format = workbook.add_format({'bold': True})
        # bold_format.font_size = 12
        # bold_format.set_align('center')
        # # 标题信息
        # head = [u"邮箱地址"]
        for i in range(0, len(tmp_list)):
            sheet.write(i, 0, tmp_list[i].get('country'))
            sheet.write(i, 1, tmp_list[i].get('province'))
            sheet.write(i, 2, tmp_list[i].get('city'))
            sheet.write(i, 3, tmp_list[i].get('county'))
            sheet.write(i, 4, tmp_list[i].get('longitude'))
            sheet.write(i, 5, tmp_list[i].get('latitude'))
        # 保存xlsx模板
        workbook.close()
    except Exception as err:
        logging.error("Erro: {}".format(err), exc_info=1)


def main():
    logging.warn('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    read_cve('D:\\script_test\\address_test.xls')


if __name__ == "__main__":
    main()
