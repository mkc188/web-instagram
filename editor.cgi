#!/usr/bin/env python
# encoding: utf-8

from string import Template
import MySQLdb
import Cookie
import os
import cgi
import cgitb
import subprocess
import tempfile
import time
import glob
import shutil
import warnings

saveDir = 'tmp/'
readDir = 'data/'

def read_template(filename):
    with open(filename, 'r') as f:
        return f.read()

def do_something(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()

def update_db(newname):
    query = 'INSERT INTO history (filename, previous) VALUES (%s, %s)'
    cursor.execute(query, [newname, s_dict['image']])
    conn.commit()
    s_dict['image'] = newname
    set_cookie(newname)

def set_cookie(new):
    expireTimestamp = time.time() + 30*24*60*60
    expireTime = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expireTimestamp))
    cookie['filename'] = new
    cookie['filename']['expires'] = expireTime
    print cookie

def get_info():
    savePath = os.path.join(saveDir, s_dict['image'])
    cmd = ['identify', savePath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    size = out.split()[2]
    return map(int, size.split('x'))

def rmfile(name):
    globname = name + '*'
    for file in glob.glob(globname):
        os.remove(file)

def cleanup(addr):
    previous = [s_dict['image']]
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

    cookie['filename']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    print cookie
    print 'Status: 302 Moved'
    print 'Location: %s\n' % addr

try:
    import traceback
    import sys
    sys.stderr = sys.stdout

    cgitb.enable()
    warnings.filterwarnings('ignore', category = MySQLdb.Warning)

    s = Template(read_template('views/editor.tpl'))
    s_dict = {'image': '', 'message': ''}

    cookie = Cookie.SimpleCookie()
    cookie_string = os.environ.get('HTTP_COOKIE')
    if cookie_string:
        cookie.load(cookie_string)
        if 'filename' in cookie:
            s_dict['image'] = cookie['filename'].value
    else:
        print 'Status: 302 Moved'
        print 'Location: %s\n' % 'index.cgi?r=0'

    dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
    dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
    dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
    dbName = os.getenv("OPENSHIFT_APP_NAME")
    conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
    cursor = conn.cursor()

    form = cgi.FieldStorage()
    if 'filter' in form:
        newname = os.path.basename(tempfile.NamedTemporaryFile(dir=saveDir).name) + s_dict['image'][-4:]
        value = form.getfirst('filter')
        width, height = get_info()
        if value == 'border':
            cmd = ['convert', saveDir+'/'+s_dict['image'], '-bordercolor', 'black', '-border', str(min(width, height)*0.05), saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
        elif value == 'lomo':
            cmd = ['convert', saveDir+'/'+s_dict['image'], '-channel', 'R', '-level', '33%', '-channel', 'G', '-level', '33%', saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
        elif value == 'lensflare':
            cmd = ['convert', 'images/lensflare.png', '-resize', str(width)+'x', saveDir+'/'+newname+'.1']
            do_something(cmd)
            cmd = ['composite', '-compose', 'screen', '-gravity', 'northwest',saveDir+'/'+newname+'.1', saveDir+'/'+s_dict['image'], saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
        elif value == 'blackwhite':
            cmd = ['convert', saveDir+'/'+s_dict['image'], '-type', 'grayscale', saveDir+'/'+newname+'.1']
            do_something(cmd)
            cmd = ['convert', 'images/bwgrad.png', '-resize', str(width)+'x'+str(height)+'!', saveDir+'/'+newname+'.2']
            do_something(cmd)
            cmd = ['composite', '-compose', 'softlight', '-gravity', 'center', saveDir+'/'+newname+'.2', saveDir+'/'+newname+'.1', saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
        elif value == 'blur':
            cmd = ['convert', saveDir+'/'+s_dict['image'], '-blur', '0.5x2', saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
    elif 'annotate' in form:
        newname = os.path.basename(tempfile.NamedTemporaryFile(dir=saveDir).name) + s_dict['image'][-4:]
        value = form.getfirst('annotate')
        message = form.getfirst('message').encode('string-escape')
        fontsize = form.getfirst('fontsize')
        font = form.getfirst('font')
        if value == 'top':
            cmd = ['convert', saveDir+'/'+s_dict['image'], '-fill', 'white', '-background', 'black', '-pointsize', fontsize, '-font', 'fonts/'+font+'.ttf', 'label:'+message, '+swap', '-gravity', 'center', '-append', saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
        elif value == 'bottom':
            cmd = ['convert', saveDir+'/'+s_dict['image'], '-fill', 'white', '-background', 'black', '-pointsize', fontsize, '-font', 'fonts/'+font+'.ttf', 'label:'+message, '-gravity', 'center', '-append', saveDir+'/'+newname]
            do_something(cmd)
            update_db(newname)
    elif 'edit' in form:
        value = form.getfirst('edit')
        tmpfn = s_dict['image']
        fn = tmpfn[3:]
        if value == 'undo':
            query = 'SELECT previous FROM history WHERE filename = %s'
            cursor.execute(query, [s_dict['image']])
            previous = cursor.fetchone()
            
            if previous:
                query = 'DELETE FROM history WHERE filename = %s'
                cursor.execute(query, [s_dict['image']])
                conn.commit()
                rmfile(saveDir+s_dict['image'])
                s_dict['image'] = previous[0]
                set_cookie(previous[0])
            else:
                s_dict['message'] = '<div class="row text-center"><div class="col-xs-12"><div class="alert alert-warning" role="alert">Already at oldest change.</div></div></div>'
        elif value == 'discard':
            cleanup('index.cgi')
        elif value == 'finish':
            query = 'INSERT INTO images (permalink) VALUES (%s)'
            cursor.execute(query, [fn])
            conn.commit()
            shutil.copyfile(saveDir+tmpfn, readDir+fn)
            cleanup('finish.cgi?i=%s' % fn)

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
