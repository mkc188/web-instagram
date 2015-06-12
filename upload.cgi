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
import glob
import warnings

saveDir = 'tmp/'
readDir = 'data/'

def read_template(filename):
    with open(filename, 'r') as f:
        return f.read()

def rmfile(name):
    globname = name + '*'
    for file in glob.glob(globname):
        os.remove(file)

try:
    import traceback
    import sys
    sys.stderr = sys.stdout

    cgitb.enable()
    warnings.filterwarnings('ignore', category = MySQLdb.Warning)

    s = Template(read_template('views/upload.tpl'))
    s_dict = {'message': '', 'next': ''}

    dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
    dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
    dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
    dbName = os.getenv("OPENSHIFT_APP_NAME")
    conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)

    form = cgi.FieldStorage()
    # saveDir = os.getenv('OPENSHIFT_DATA_DIR')
    if ('pic' not in form):
        s_dict['message'] += '<div class="alert alert-danger" role="alert">No file uploaded.</div>'
    elif (not form['pic'].filename):
        s_dict['message'] += '<div class="alert alert-danger" role="alert">No file selected.</div>'
    else:
        fileitem = form['pic']
        (fn, ext) = os.path.splitext(os.path.basename(fileitem.filename))
        fn = os.path.basename(tempfile.NamedTemporaryFile(dir=saveDir).name)
        savePath = os.path.join(saveDir, fn + ext)

        open(savePath, 'wb').write(fileitem.file.read())

        cmd = ['identify', savePath]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        try:
            filetype = out.split()[1]
            ft_dict = {'jpeg':'jpg', 'gif':'gif', 'png':'png'}
            ft = ft_dict[filetype.lower()]
        except:
            ft = None
        if ft != ext[1:].lower():
            s_dict['message'] += '<div class="alert alert-danger" role="alert">Invalid file type.</div>'
            rmfile(savePath)
        else:
            query = 'INSERT INTO sessions (filename) VALUES (%s)'
            cursor = conn.cursor()
            cursor.execute(query, [fn+ext])
            conn.commit()

            s_dict['message'] += '<div class="alert alert-success" role="alert">' + 'File "' + fileitem.filename + '" uploaded.' + '</div>'
            s_dict['next'] = '<a class="btn btn-primary" href="editor.cgi" role="button">Next</a>'
            s_dict['message'] += '<img class="img-responsive center-block" src="%s">' % (os.path.join(saveDir, fn + ext))

            cookie = Cookie.SimpleCookie()
            cookie_string = os.environ.get('HTTP_COOKIE')
            if cookie_string:
                cookie.load(cookie_string)
                if 'filename' in cookie:
                    previous = [cookie['filename'].value]
                    removed = ''
                    while previous:
                        rmfile(saveDir+previous[0])
                        removed = previous[0]
                        query = 'SELECT previous FROM history WHERE filename = %s'
                        cursor.execute(query, [previous[0]])
                        previous = cursor.fetchone()
                        query = 'DELETE FROM history WHERE filename = %s'
                        cursor.execute(query, [removed])
                        conn.commit()

                    rmfile(saveDir+removed)
                    query = 'DELETE FROM sessions WHERE filename = %s'
                    cursor.execute(query, [removed])
                    conn.commit()

            cursor.close()

            expireTimestamp = time.time() + 30*24*60*60
            expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))
            cookie['filename'] = fn + ext
            cookie['filename']['expires'] = expireTime
            print cookie

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
