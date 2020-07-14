#! -*- coding: utf-8 -*-
import logging

from flask.views import MethodView
from flask import request, render_template
from model_test.antapt import AntaptDatabase
from model_test.model import Cvelib

db = AntaptDatabase().session


class CveView(MethodView):

    def get(self):
        cve_id = request.args.get('cve_id', '')

        cve_info = None
        if cve_id:
            logging.info(cve_id)
            cve = db.query(Cvelib).filter_by(cve_id=cve_id.encode('utf-8')).first()
            cve_info = cve.as_dict() if cve else None
            logging.info(cve_info)
        return render_template('cve.html', cve_info=cve_info)
        # cve_count = db.query(Cvelib).count()


class CveHomeView(MethodView):

    def get(self):

        return render_template('cve_home.html')

