import cherrypy
import os, os.path
from mako.template import Template
import pymysql.cursors

SERVER_PORT = 8001
SERVER_HOST = '127.0.0.1'

# В качестве примера SQL инъекции введём например: @@@' UNION SELECT 1, CONCAT('Username: ', username, '</br>Email: ', email, '</br>Password hash: ', `password`) FROM auth_user -- 

class SqlInjectionServer(object):
    @cherrypy.expose
    def index(self, search_text = None):
        database = pymysql.connect(host='localhost',
                                         user='labs',
                                         password='0000',
                                         db='labs',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)
        mytemplate = Template(filename='static/template/index.html')
        with database.cursor() as cursor:
            if search_text is None:
                sql = "SELECT title, text FROM news"
            else:
                sql = "SELECT title, text FROM news WHERE text LIKE '%" + search_text + "%'"
            cursor.execute(sql)
            result = cursor.fetchall()
        return mytemplate.render(news = result)

cherrypy.config.update({
    'server.socket_host': SERVER_HOST,
    'server.socket_port': SERVER_PORT,
})

path = os.path.abspath(os.getcwd())
conf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': path
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': path + '/static'
    }
}
cherrypy.quickstart(SqlInjectionServer(), '/', conf)