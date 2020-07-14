#! -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import request, render_template


class LoginView(MethodView):

    def post(self):
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            return render_template('signin-ok.html', username=username)
        return render_template('form.html', message='Bad username or password', username=username)

    def get(self):
        return render_template('form.html')


class HomeView(MethodView):

    def get(self):
        return render_template('index.html')
