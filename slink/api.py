import pymysql
from tornado_json.requesthandlers import APIHandler
import string
import random
import re
import datetime


class LinksAPIHandler(APIHandler):
    __url_names__ = ["links"]

class GetLinks(LinksAPIHandler):
    def get(self):
        try:

            User = self.get_argument("User")
            conn = pymysql.connect(host='localhost', port=3306, user='user', passwd='1qaz@WSX', db='link_short')
            cur = conn.cursor()
            cur.execute("SELECT DateCreat, Link, LinkShort, linkscol FROM links WHERE user = '" + User + "'")
            cur.close()
            conn.close()
            list1 = []
            for row in cur:
                Data2 = {"Date": str(row[0]), "Link": str(row[1]), "ShortLink": str(row[2]), "Kol": row[3]}

                list1.append(Data2)
            Data = tuple(list1)

            self.success(Data)
        except KeyError:
            self.fail("fail")





class SlinkAPIHandler(APIHandler):
    __url_names__ = ["slink"]


class MakeListHandler(SlinkAPIHandler):

    def get(self):
        try:

            shortlink = self.get_argument("ShortLink")
            conn1 = pymysql.connect(host='localhost', port=3306, user='user', passwd='1qaz@WSX', db='link_short')
            cur1 = conn1.cursor()
            sql = "SELECT Link  FROM links WHERE LinkShort = '" + shortlink + "'"
            cur1.execute(sql)
            cur1.close()
            conn1.close()

            if cur1.rowcount != 0:
                link = cur1._rows[0]
                DATA = {'Link': link[0]}
                self.success(DATA)
            return
        except KeyError:
            self.fail("fail")


class MakeAPIHandler(SlinkAPIHandler):
    def get(self, User):
        try:
            link = self.get_argument("Link")
            conn2 = pymysql.connect(host='localhost', port=3306, user='user', passwd='1qaz@WSX', db='link_short')
            cur2 = conn2.cursor()
            sql = "SELECT LinkShort FROM links WHERE Link = '" + link + "'"
            cur2.execute(sql)
            cur2.close()
            conn2.close()
            if cur2.rowcount == 0:
                reg = re.compile('[^a-zA-Z ]')

                short_link = generator_short_link(6, reg.sub('', link))
                now = str(datetime.datetime.now())
                DATA = {'ShortLink': short_link}

                conn3 = pymysql.connect(host='localhost', port=3306, user='user', passwd='1qaz@WSX', db='link_short')
                cur3 = conn3.cursor()
                sql = "Insert into  links (Link, LinkShort, User, DateCreat, linkscol) values ('" + link + "', '" + short_link + "', '" + User + "', '" + now + "', 0)"
                cur3.execute(sql)
                conn3.commit()
                cur3.close()
                conn3.close()
                self.success(DATA)
                return
            else:
                self.fail("Такая ссылка уже сокращена - " + str(cur._rows[0]))
        except KeyError:
            self.fail("No data on such make `{}`.".format(Link))

def generator_short_link(size: object = 6, chars: object = string.ascii_uppercase + string.digits) -> object:
    return ''.join(random.choice(chars) for _ in range(size))


    

