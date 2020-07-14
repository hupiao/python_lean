# -*- coding:utf-8 -*-
import  xlsxwriter
from datetime import datetime
from apps.db.mypsgres import MyPsgres
from apps.db.db import User

#=======  连接本地pg  ======#
ps = MyPsgres(
    database='flask_learn',
    user='postgres',
    pwd='123456',
    host='192.168.217.133')

users = ps.session.query(User).all()

users = ps.session.query(User).order_by(User.id.asc()).all()
xls = xlsxwriter.Workbook('E:\test_data\测试test.xlsx')
sheet = xls.add_worksheet("test")  # 创建一个test的表

header = [ u'姓名', u'密码', u'创建时间',u'文件名']# 设置表头
header_db = ['name', 'password', 'create_time', 'file_name']

header_property = {
    'font_size': 15,  # 字体大小
    'bold': True,  # 是否加粗
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'font_name': u'微软雅黑',
    'text_wrap': False,  # 是否自动换行
    'font_color': 'red'
}
header_format = xls.add_format(header_property)
sheet.write_row('A1', header, header_format)

cell_property = {
    'font_size': 11,  # 字体大小
    'bold': False,  # 是否加粗
    'align': 'left',  # 水平对齐方式
    'valign': 'vcenter',  # 垂直对齐方式
    'font_name': u'微软雅黑',
    'text_wrap': False,  # 是否自动换行
}
cell_format = xls.add_format(cell_property)
row = 1
column_num = header.__len__()
for user in users:
    column = 0
    for column in range(column_num):
        print(getattr(user, header_db[column]))
        sheet.write(row, column, getattr(user, header_db[column]), cell_format)
    row = row+1
xls.close()
now_str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
file_name = "列表" + "_" + now_str
xlsx_file = '%s.xlsx' % (file_name)
print(xlsx_file)

