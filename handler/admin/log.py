#!/usr/bin/env python
# coding:utf-8

from tornado.web import authenticated
from base import BaseHandler
from optsql.db import db


class LoginHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        if not self.current_user:
            self.render('admin/login.html')

        else:
            self.redirect('test/admin/vote_accounts', permanent=True)

    def post(self):
        name = self.get_argument('name')
        pwd = self.get_argument('pwd')

        rlt = db.get('select * from user where username="%s" and password="%s"' % (name, pwd))

        if rlt is None:
            self.write(u'登陆失败，请尝试刷新页面重新登陆')

        else:
            self.set_secure_cookie('user', str(rlt.id))
            self.redirect('/vote_accounts', permanent=True)


class LogoutHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @authenticated
    def get(self):
        self.clear_cookie('user')
        self.redirect('test/admin/login', permanent=True)
