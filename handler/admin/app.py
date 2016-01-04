#!/usr/bin/env python
# coding:utf-8
import json
import os
import uuid
import MySQLdb
from qiniu import Auth, put_data

from base import BaseHandler
import config
from optsql.db import db


class AppQueryHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        rows = db.query("SELECT * FROM app")

        self.render('admin/apps.html', rows=rows)


class AppEditHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, action):
        if action == 'add':
            self.render('admin/app_edit.html', action=action)

        elif action == 'edit':
            app_id = int(self.get_argument('app_id', 1))
            app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

            if app is None:
                self.write(u'找不到该 APP')
                return

            self.render('admin/app_edit.html', action=action, app=app)

        elif action == 'delete':
            app_id = int(self.get_argument('app_id', 1))
            app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

            if app is None:
                self.write(json.dumps(dict(flag=False, message='未找到该 APP')))
                return

            sql = "DELETE FROM app WHERE id=%d" % app_id
            db.delete(sql)

            self.write("删除成功")

    def post(self, action):
        self.set_header('Content-Type', 'text/json')

        if action == 'add':
            qrcode_url = self.get_file_uploaded_url('qrcode_url')
            if qrcode_url is None:
                self.write(json.dumps(dict(flag=False, message='图片上传到七牛失败')))
                return

            bg_url = self.get_file_uploaded_url('bg_url')
            if bg_url is None:
                self.write(json.dumps(dict(flag=False, message='图片上传到七牛失败')))
                return

            sql = "INSERT INTO app(name, qrcode_url, bg_url, question, intro, input_label, " \
                  "answer_prefix, uid, follow_tip, retest_tip, pv, fake_pv, active) " \
                  "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, '%s', '%s', %d, %d, %d)" \
                  % (MySQLdb.escape_string(self.get_body_argument('name')),
                     MySQLdb.escape_string(qrcode_url),
                     MySQLdb.escape_string(bg_url),
                     MySQLdb.escape_string(self.get_body_argument('question')),
                     MySQLdb.escape_string(self.get_body_argument('intro')),
                     MySQLdb.escape_string(self.get_body_argument('input_label')),
                     '', 1,
                     MySQLdb.escape_string(self.get_body_argument('follow_tip')),
                     MySQLdb.escape_string(self.get_body_argument('retest_tip')),
                     0, int(self.get_body_argument('fake_pv')), True)

            db.insert(sql)
            self.write(json.dumps(dict(flag=True, url='/test/admin/app')))

        elif action == 'edit':
            app_id = int(self.get_argument('app_id', 1))
            app = db.get('SELECT * FROM app WHERE id=%d' % app_id)

            if app is None:
                self.write(json.dumps(dict(flag=False, message='未找到该 APP')))
                return

            qrcode_url = self.get_file_uploaded_url('qrcode_url')
            if qrcode_url is None:
                self.write(json.dumps(dict(flag=False, message='图片上传到七牛失败')))
                return
            elif qrcode_url == '':
                qrcode_url = app.qrcode_url

            bg_url = self.get_file_uploaded_url('bg_url')
            if bg_url is None:
                self.write(json.dumps(dict(flag=False, message='图片上传到七牛失败')))
                return
            elif bg_url == '':
                bg_url = app.bg_url

            sql = "UPDATE app SET name='%s', qrcode_url='%s', bg_url='%s', " \
                  "question='%s', intro='%s', input_label='%s', follow_tip='%s', retest_tip='%s', " \
                  "fake_pv=%d WHERE id=%d" \
                  % (MySQLdb.escape_string(self.get_body_argument('name')),
                     MySQLdb.escape_string(qrcode_url),
                     MySQLdb.escape_string(bg_url),
                     MySQLdb.escape_string(self.get_body_argument('question')),
                     MySQLdb.escape_string(self.get_body_argument('intro')),
                     MySQLdb.escape_string(self.get_body_argument('input_label')),
                     MySQLdb.escape_string(self.get_body_argument('follow_tip')),
                     MySQLdb.escape_string(self.get_body_argument('retest_tip')),
                     int(self.get_body_argument('fake_pv')),
                     app_id)

            db.update(sql)
            self.write(json.dumps(dict(flag=True, url='/test/admin/app')))

    def get_file_uploaded_url(self, name):
        if name in self.request.files:
            fileinfo = self.request.files[name][0]
            fname = fileinfo['filename']
            body = fileinfo['body']

            extn = os.path.splitext(fname)[1]
            cname = str(uuid.uuid4()) + extn

            q = Auth(config.QINIU_AK, config.QINIU_SK)
            key = 'upload/' + cname
            token = q.upload_token(config.QINIU_BUCKET_NAME)
            ret, info = put_data(token, key, body)

            if info.status_code == 200:
                return 'http://7xon5f.com2.z0.glb.qiniucdn.com/' + key
            else:
                return None

        return ''

