#!/opt/work/.pyenv/versions/vid/bin/python
# -*-coding: utf-8 -*-

import os
import sys
import posixpath
import logging

# Fix some apache issues when PATH does not exist,
# This will make python 2.7 + virtualenv load fail.
os.environ.setdefault('PATH', '')

# 激活独立的python运行环境
activate_this = '/opt/work/.pyenv/versions/vid/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# os.environ['PYTHON'] = '/opt/work/web/env/bin/python2.7'
# os.environ['PYTHON_EGG_CACHE'] = '/tmp'
# #os.environ['SETTINGS_MODULE'] = 'xenopsapi.settings'

os.environ['PYTHON'] = '/opt/work/.pyenv/versions/vid/bin/python'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['VID_ENV'] = 'production'
sys.path.append('/opt/work/web')

from app import create_app # noqa
application = create_app()

# The following code fix the script to make it works with mod_rewrite.

_application = application


def application(environ, start_response):
    # Wrapper to set SCRIPT_NAME to actual mount point,
    # usually means mod_rewrite is used.
    script_name = environ['SCRIPT_NAME']
    if script_name.endswith('.wsgi') or script_name.endswith('.fcgi'):
        environ['SCRIPT_NAME'] = posixpath.dirname(script_name)
    if environ['SCRIPT_NAME'] == '/':
        environ['SCRIPT_NAME'] = ''
    #logging.info(environ)
    return _application(environ, start_response)


if __name__ == '__main__':
    from flup.server.fcgi import WSGIServer  # noqa
    WSGIServer(application, bindAddress='/opt/work/web/www/webapi-fastcgi.sock', umask=000).run()
