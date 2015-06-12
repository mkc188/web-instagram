#!/usr/bin/env python
# encoding: utf-8

from string import Template
import os
import sys
import cgi
import cgitb
import tempfile
import MySQLdb
import Cookie
import time
import subprocess
import warnings

saveDir = 'tmp/'
readDir = 'data/'

def read_template(filename):
    with open(filename, 'r') as f:
        return f.read()

try:
    import traceback
    import sys
    sys.stderr = sys.stdout

    cgitb.enable()
    warnings.filterwarnings('ignore', category = MySQLdb.Warning)

    s = Template(read_template('views/finish.tpl'))
    s_dict = {'message': ''}

    form = cgi.FieldStorage()
    img = form.getfirst('i')
    if 'i' in form and os.path.isfile(readDir+img):
        s_dict['message'] += '<div class="alert alert-success" role="alert">http://%s/data/%s</div>' % (os.getenv("OPENSHIFT_APP_DNS"), img)
        s_dict['message'] += '<img class="img-responsive center-block" src="%s">' % (os.path.join(readDir, img))
    else:
        print 'Status: 302 Moved'
        print 'Location: %s\n' % 'index.cgi'

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
