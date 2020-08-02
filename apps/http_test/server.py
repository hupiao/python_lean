from flask import Flask, send_file
from flask.views import MethodView

app = Flask(__name__)


class FileViews(MethodView):

    def get(self):
        return send_file('/opt/work/pyenv_empty.tar.gz')


testview = FileViews.as_view('test')
app.add_url_rule('/test/', view_func=testview, methods=['GET'])
# app.config.from_pyfile('settings.py')
app.config["DEBUG"]=True
app.run(host='127.0.0.1', port=5000)
