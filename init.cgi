#!/usr/bin/env python
# encoding: utf-8

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

def remove_file(dir):
    files = os.listdir(dir)
    for f in files:
        os.remove(os.path.join(dir, f))

try:
    import traceback
    import sys
    sys.stderr = sys.stdout

    cgitb.enable()
    warnings.filterwarnings('ignore', category = MySQLdb.Warning)

    dbHost = os.getenv("OPENSHIFT_MYSQL_DB_HOST")
    dbUser = os.getenv("OPENSHIFT_MYSQL_DB_USERNAME")
    dbPass = os.getenv("OPENSHIFT_MYSQL_DB_PASSWORD")
    # dbName = os.getenv("OPENSHIFT_APP_NAME")
    conn = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass)
    cursor = conn.cursor()

    remove_file(saveDir)
    remove_file(readDir)

    query = '''
        SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
        SET GLOBAL time_zone = "+8:00";
        CREATE DATABASE IF NOT EXISTS `webig` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
        USE `webig`;
        CREATE TABLE IF NOT EXISTS `images` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `permalink` text NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        TRUNCATE TABLE `images`;
        CREATE TABLE IF NOT EXISTS `sessions` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `filename` text NOT NULL,
        `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        TRUNCATE TABLE `sessions`;
        CREATE TABLE IF NOT EXISTS `history` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `filename` TEXT NOT NULL,
        `previous` TEXT NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        TRUNCATE TABLE `history`
    '''
    for q in query.split(';'):
        cursor.execute(q.strip(), [])
    conn.commit()
    cursor.close()
    conn.close()

    cookie = Cookie.SimpleCookie()
    cookie_string = os.environ.get('HTTP_COOKIE')
    if cookie_string:
        cookie.load(cookie_string)
        if 'filename' in cookie:
            cookie['filename']['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
            print cookie

    print 'Status: 302 Moved'
    print 'Location: %s\n' % 'index.cgi?s=1'

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
