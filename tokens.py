import threading
import time
import random
from optsql.db import db


class TokensRefreshTask(threading.Thread):
    def __init__(self):
        super(TokensRefreshTask, self).__init__()

    def run(self):
        try:
            while True:
                apps = db.query("SELECT * FROM app;")
                for app in apps:
                    db.update("UPDATE app SET token=%d WHERE id=%d" % (random.randint(1, 99999), app.id))

                time.sleep(300)
        except Exception, e:
            print Exception, ':', e


