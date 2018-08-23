import pymysql
#from configparser import ConfigParser


def getconnection():

    connection = pymysql.connect(host='localhost',
                                 user='user',
                                 passwd='1qaz@WSX',
                                 db='link_short')
    return connection


 
 
#def read_db_config(filename='config.ini', section='mysql'):

    #parser = ConfigParser()
    #parser.read(filename)
 
    #db = {}
    #if parser.has_section(section):
        #items = parser.items(section)
        #for item in items:
            #db[item[0]] = item[1]
    #else:
        #raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    #return db
