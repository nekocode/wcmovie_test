#!/usr/bin/env python
# coding:utf-8

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    # def get_current_user(self):
    #     return self.get_secure_cookie('user')

