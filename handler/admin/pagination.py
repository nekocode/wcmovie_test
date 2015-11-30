__author__ = 'nekocode'


class Pagination:
    def __init__(self, db, per_page_count):
        self.db = db
        self.per_page_count = per_page_count

    def get_page_rows(self, p, table_name, where=''):
        # 获取分页数量
        row_count = self.db.get("SELECT COUNT(*) FROM %s %s" % (table_name, where))['COUNT(*)']
        page_count = row_count/self.per_page_count + 1
        if row_count % self.per_page_count == 0:
            page_count -= 1

        if p < 1 or p > page_count:
            p = 1

        if page_count <= 5:
            pages = range(1, page_count+1)
        else:
            if p <= 3:
                pages = range(1, 6)
            elif p > page_count-2:
                pages = range(page_count-4, page_count+1)
            else:
                pages = range(p-2, p+2)

        # 获取分页
        rows = self.db.query("SELECT * FROM %s %s ORDER BY id DESC LIMIT %d,%d"
                                   % (table_name, where, self.per_page_count*(p-1), self.per_page_count))

        return p, rows, pages


