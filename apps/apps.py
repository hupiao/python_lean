# -*- coding: utf-8 -*
import os
import xlsxwriter
from os import path
from collections import OrderedDict

from flask import render_template, Flask, request, Response, jsonify
from flask import after_this_request
from flask.views import MethodView
from xml.etree import ElementTree as et
from werkzeug.utils import secure_filename  # 使用这个是为了确保filename是安全的

# from apps.db.mypsgres import MyPsgres
# from apps.db.db import User

app = Flask(__name__)


class TestViews(MethodView):
    def get(self):

        @after_this_request
        def mod(response):
            # response.set_cookie('name', 'hupiao')
            return response
        # return "hello world"

        # URL params
        # print(type(request.args))
        # print(request.args.to_dict())
        # data, errors = UserSchema().load(request.args)
        # print(data)
        # print(errors)
        # print(request.remote_addr)
        # print(current_app.config.get('NAME'))
        # age = str(request.args.get('age'))
        # print(type(age))
#==============# 导出列表
        ps = MyPsgres(
            database='flask_learn',
            user='postgres',
            pwd='123456',
            host='192.168.217.133')

        users = ps.session.query(User).order_by(User.id.asc()).all()
        # out = BytesIO()
        path = 'E:/test_data/'
        filename = u'测试'+'_'+'.xlsx'
        # print(os.path.join(path,filename))
        xls = xlsxwriter.Workbook(path +filename)
        sheet = xls.add_worksheet("test")  # 创建一个test的表

        header = [u'姓名', u'密码', u'创建时间', u'文件名']  # 设置表头
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
                sheet.write(row, column, str(getattr(user, header_db[column])), cell_format)
            row = row + 1
        xls.close()
        # out.seek(0)
        # return send_from_directory(path, filename, as_attachment=True)
        # response = make_response(send_from_directory(path, filename.decode('latin-1'), as_attachment=True))
        # response.headers['Content-Disposition'] += "; filename*=utf-8''{}".format(filename)
        #
        # return response
        return ""

    def post(self):
        # form params
        # name = request.form['name']
        # age = request.form['age']
        # dic = {"name": name, "age": age}
        # return json.dumps(dic)

        test_column = request.json.get('test')
        print(type(test_column))
        return "ok"

    def put(self):
        # # json, text params
        # a = request.get_data()
        # dic = json.loads(a)
        # # print(type(dic))
        # name = dic['name']
        # age = dic['age']
        # dic1 = {"name": name, "age": age}
        # # print(type(str(name)))
        # # return html
        # return '<h1>数据已接收</h1>'

        # xml params
        xm = request.get_data()
        root = et.XML(xm)
        # print(root.tag)
        # 遍历节点
        for node in root:
            # 节点的标签名称和内容
            print(node.tag, node.text)
        # print(type(xm))
        return '<h1>数据已接收</h1>'


@app.route("/form/new", methods=['POST'])
def new_form():
    # multipart/form-data
    #save file
    f = request.files["file"]
    base_path = path.abspath(path.dirname(__file__))
    upload_path = path.join(base_path, 'static/uploads/')
    if not path.exists(upload_path):
        os.mkdir(path)
    file_name = upload_path + secure_filename(f.filename)
    f.save(file_name)
    return Response(u'已经保存')


@app.route('/')
def index():
    # rsp =Response(response=render_template('test.html'), status=0)
    # rsp.set_cookie('name','hupiao')
    d = OrderedDict()
    d['a'] = 'a'
    d['c'] = 'c'
    d['b'] = 'b'
    import json
    return json.dumps({'data': d, 'status': 200})
    # return render_template('post.html')


testview = TestViews.as_view('test')
app.add_url_rule('/test/', view_func=testview, methods=['GET', 'POST', 'PUT'])
app.config.from_pyfile('settings.py')
app.run(host='127.0.0.1', port=5000, debug=True)



