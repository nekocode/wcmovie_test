#!/usr/bin/env python
# coding:utf-8

from tornado import escape
from tornado.web import authenticated
from base import BaseHandler, pagination
from optsql.db import db


class AnswerQueryHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @authenticated
    def get(self):
        uid = int(escape.xhtml_escape(self.current_user))
        app_id = int(self.get_argument('app_id', 1))
        app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

        if app is None or app.uid != uid:
            self.write(u'你没有权限访问该 APP')
            return

        p = int(self.get_argument('p', 1))
        rows = pagination.get_page_rows(p, 'answer', 'WHERE app_id=%d' % app_id)


class AnswerEditHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @authenticated
    def get(self, action):
        uid = int(escape.xhtml_escape(self.current_user))
        answer_id = int(self.get_argument('answer_id', 1))
        answer = db.get('SELECT * FROM answer WHERE id=%d' % answer_id)
        app = db.get('SELECT * FROM app WHERE id=%d' % answer.app_id)

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
        answer_id = int(self.get_argument('answer_id', 1))
        answer = db.get('SELECT * FROM answer WHERE id=%d' % answer_id)
        app = db.get('SELECT * FROM app WHERE id=%d' % answer.app_id)

        if app is None or app.uid != uid:
            self.write(u'你没有权限访问该 APP')
            return

        if action == 'add':
            pass
        elif action == 'edit':
            pass


class AnswerCountPageHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @authenticated
    def get(self):
        pass




