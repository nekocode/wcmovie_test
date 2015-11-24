#!/usr/bin/env python
# coding:utf-8

import sys
from handler.test import TestHandler

reload(sys)
sys.setdefaultencoding('utf-8')


url = [
    (r'/test/(.*)', TestHandler),
]
