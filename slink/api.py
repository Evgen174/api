import string
import random
import re
import datetime

from tornado_json.requesthandlers import APIHandler
from python_mysql_dbconfig import getconnection




class LinksAPIHandler(APIHandler):# pylint: disable=too-few-public-methods
    __url_names__ = ["links"]

class GetLinks(LinksAPIHandler):# pylint: disable=too-few-public-methods
    def post(self):
        try:
            user_name = self.get_argument("User")
            conn = getconnection()
            cur = conn.cursor()
            cur.execute("SELECT DateCreat, Link, LinkShort, linkscol "
                        "FROM links WHERE user = %s;", (user_name))
            cur.close()
            conn.close()
            list_links = []
            for row in cur:
                list_links.append({
                    "Date": str(row[0]),
                    "Link": str(row[1]),
                    "ShortLink": str(row[2]),
                    "Kol": row[3]
                })
            self.success(tuple(list_links))
        except KeyError:
            self.fail("Fail")





class GetLinkAPIHandler(APIHandler):# pylint: disable=too-few-public-methods
    __url_names__ = ["getlink"]


class GetLinkHandler(GetLinkAPIHandler):# pylint: disable=too-few-public-methods

    def get(self):
        try:
            shortlink = self.get_argument("ShortLink")
            conn = getconnection()
            cur = conn.cursor()
            cur.execute("SELECT Link  FROM links WHERE LinkShort = %s;", (shortlink))
            cur.close()
            conn.close()
            if cur.rowcount != 0:
                row_value = cur._rows[0]#pylint: disable=protected-access
                self.success({'Link': row_value[0]})
            else:
                self.fail("No link")
            return
        except KeyError:
            self.fail("Fail")

class SlinkAPIHandler(APIHandler):# pylint: disable=too-few-public-methods
    __url_names__ = ["slink"]

class MakeAPIHandler(SlinkAPIHandler):# pylint: disable=too-few-public-methods
    def post(self):
        try:
            user = self.get_argument("User")
            link = self.get_argument("Link")
            conn = getconnection()
            cur = conn.cursor()
            cur.execute("SELECT LinkShort FROM links WHERE Link = %s ", (link))
            if cur.rowcount == 0:
                reg = re.compile('[^a-zA-Z ]')
                while True:
                    short_link = generator_short_link(6, reg.sub('', link))
                    cur.execute("SELECT Link FROM links WHERE LinkShort = %s ", (short_link))
                    if cur.rowcount == 0:
                        break
                now = str(datetime.datetime.now())
                cur.execute("INSERT INTO  links (linkscol, Link, LinkShort, User, DateCreat) "
                            "VALUES (0, %s, %s,%s,%s);", (link, short_link, user, now))
                conn.commit()
                cur.close()
                conn.close()
                answer_shortlink = {'ShortLink': short_link}
                self.success(answer_shortlink)
            else:
                self.fail("This link already exists")
        except KeyError:
            self.fail("Error in creating a link")

def generator_short_link(size: object = 6,
                         chars: object = string.ascii_uppercase + string.digits) -> object:
    return ''.join(random.choice(chars) for _ in range(size))
