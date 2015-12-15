#!/usr/bin/env python
# coding:utf-8

from tornado import escape
from tornado.web import authenticated
from base import BaseHandler, pagination
from optsql.db import db


class AppQueryHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        p = int(self.get_argument('p', 1))
        rows = pagination.get_page_rows(p, 'app')

        self.render('admin/apps.html', rows=rows)


class AppEditHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, action):
        app_id = int(self.get_argument('app_id', 1))
        app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

        if app is None:
            self.write(u'找不到该 APP')
            return

        if action == 'add':
            self.render('admin/app_edit.html')
        elif action == 'edit':
            self.render('admin/app_edit.html')

    def post(self, action):
        app_id = int(self.get_argument('app_id', 1))
        app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

        if app is None:
            self.write(u'找不到该 APP')
            return

        if action == 'add':
            pass
        elif action == 'edit':
            pass


