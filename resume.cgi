#!/usr/bin/env python
# encoding: utf-8

import cgi
import cgitb

try:
    import traceback
    import sys
    sys.stderr = sys.stdout

    cgitb.enable()

    print 'Status: 302 Moved'
    print 'Location: %s\n' % 'editor.cgi'

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
