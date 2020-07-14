#! -*- coding: utf-8 -*-
import os
# import sys

# Fix some apache issues when PATH does not exist,
# This will make python 2.7 + virtualenv load fail.
os.environ.setdefault('PATH', '')

activate_this = '/opt/work/.pyenv/versions/vid/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

os.environ['PYTHON'] = '/opt/work/.pyenv/versions/vid/bin/python'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

# 使用时打开注释代码
# sys.path.append('/opt/work/web')
# from app import create_app
# app = create_app()
#
#
# if __name__ == "__main__":
#     from werkzeug.middleware.proxy_fix import ProxyFix
#     app.wsgi_app = ProxyFix(app.wsgi_app)
#     app.run()
