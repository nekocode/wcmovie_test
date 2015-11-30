#!/usr/bin/env python
# coding:utf-8

from tornado import escape
from tornado.web import authenticated
from base import BaseHandler, pagination
from optsql.db import db


class AppQueryHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @authenticated
    def get(self):
        uid = int(escape.xhtml_escape(self.current_user))

        p = int(self.get_argument('p', 1))
        p, rows, pages = pagination.get_page_rows(p, 'app', 'WHERE uid=%d' % uid)


class AppEditHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @authenticated
    def get(self, action):
        uid = int(escape.xhtml_escape(self.current_user))
        app_id = int(self.get_argument('app_id', 1))
        app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

        if app is None or app.uid != uid:
            self.write(u'你没有权限访问该 APP')
            return

        if action == 'add':
            pass
        elif action == 'edit':
            pass

    @authenticated
    def post(self, action):
        uid = int(escape.xhtml_escape(self.current_user))
        app_id = int(self.get_argument('app_id', 1))
        app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

        if app is None or app.uid != uid:
            self.write(u'你没有权限访问该 APP')
            return

        if action == 'add':
            pass
        elif action == 'edit':
            pass


