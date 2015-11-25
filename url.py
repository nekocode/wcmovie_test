#!/usr/bin/env python
# coding:utf-8

import sys
from handler.test import TestHandler, ResultHandler

reload(sys)
sys.setdefaultencoding('utf-8')


url = [
    (r'/test/(.*)/result', ResultHandler),
    (r'/test/(.*)', TestHandler),
]
