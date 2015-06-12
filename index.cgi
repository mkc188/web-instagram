#!/usr/bin/env python
# encoding: utf-8

from string import Template
import MySQLdb
import cgi
import math
import Cookie
import os
import cgitb
import warnings

saveDir = 'tmp/'
readDir = 'data/'

def read_template(filename):
    with open(filename, 'r') as f:
        return f.read()

def print_image(s_dict, images, total):
    page = cgi.FieldStorage().getfirst('p')
    if not page:
        start = 0
    else:
        start = (int(page)-1)*8
    if total > start:
        for image in images[start:start+4]:
            s_dict['imgrow1'] += '<div class="col-xs-12 col-sm-6 col-md-3 vertical-center"><a href="data/%s"><img class="img-responsive center-block" src="data/%s" height="200" width="200"></div></a>' % (image[1], image[1])
    if total > start+4:
        for image in images[start+4:start+8]:
            s_dict['imgrow2'] += '<div class="col-xs-12 col-sm-6 col-md-3 vertical-center"><a href="data/%s"><img class="img-responsive center-block" src="data/%s" height="200" width="200"></div></a>' % (image[1], image[1])

def print_page(s_dict, total):
    pages = int(math.ceil(total / 8.0))
    s_dict['pages'] = pages if pages else 1
    
    page = cgi.FieldStorage().getfirst('p')
    if page:
        page = int(page)
        if page > 1:
            s_dict['prev'] = '<li><a href="index.cgi?p=%s">Previous</a></li>' % str(page-1)
        if page < pages:
            s_dict['next'] = '<li><a href="index.cgi?p=%s">Next</a></li>' % str(page+1)
    elif pages > 1:
        s_dict['next'] = '<li><a href="index.cgi?p=2">Next</a></li>'

    for i in range(s_dict['pages']):
        if page == i+1:
            s_dict['page'] += '<option selected>%s</option>' % str(i+1)
        else:
            s_dict['page'] += '<option>%s</option>' % str(i+1)

def print_noresume(s_dict):
    message = cgi.FieldStorage().getfirst('r')
    if message == '0':
        cookie = Cookie.SimpleCookie()
        cookie_string = os.environ.get('HTTP_COOKIE')
        if cookie_string:
            cookie.load(cookie_string)
            if 'filename' in cookie:
                return
        else:
            s_dict['message'] = '<div class="row text-center"><div class="col-xs-12"><div class="alert alert-warning" role="alert">No existing session.</div></div></div>'

def print_init(s_dict):
    init = cgi.FieldStorage().getfirst('s')
    referer = os.getenv('HTTP_REFERER')
    from_init = 0
    if referer:
        from_init = referer.find('init.html')
    if init == '1' and from_init:
        s_dict['message'] = '<div class="row text-center"><div class="col-xs-12"><div class="alert alert-success" role="alert">System initialization is completed.</div></div></div>'
        return 1
    return 0

def print_noimage(s_dict):
    if s_dict['imgrow1'] == '':
        s_dict['message'] = '<div class="row text-center"><div class="col-xs-12"><div class="alert alert-warning" role="alert">No images here. Please upload one first.</div></div></div>'

try:
    import traceback
    import sys
    sys.stderr = sys.stdout

    cgitb.enable()
    warnings.filterwarnings('ignore', category = MySQLdb.Warning)

    s = Template(read_template('views/index.tpl'))
    s_dict = {'imgrow1': '', 'imgrow2': '', 'page': '', 'pages': '', 'prev': '', 'next':'', 'message': ''}

    dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
    dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
    dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
    dbName = os.getenv("OPENSHIFT_APP_NAME")
    conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
    cursor = conn.cursor()
    query = 'SELECT * FROM images'
    cursor.execute(query)
    total_image = cursor.rowcount
    images = cursor.fetchall()
    print_image(s_dict, images[::-1], total_image)
    print_page(s_dict, total_image)
    if print_init(s_dict):
        pass
    else:
        print_noimage(s_dict)
    print_noresume(s_dict)
    cursor.close()
    conn.close()

    print 'Content-type: text/html\n'
    print s.safe_substitute(s_dict)

except Exception as e:
    import traceback
    print 'Content-type: text/html\n'
    print
    print '<html><head><title>'
    print str(e)
    print '</title>'
    print '</head><body>'
    print '<h1>TRACEBACK</h1>'
    print '<pre>'
    traceback.print_exc()
    traceback.prunt_stack()
    print '</pre>'
    print '</body></html>'
