#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import cgi
import HTML
from datetime import datetime, timedelta
from wmflabs import db

if 'QUERY_STRING' in os.environ:
        QS = os.environ['QUERY_STRING']
        qs = cgi.parse_qs(QS)
        try:
                lang = qs['lang'][0]
        except:
                lang = "cs"
        try:
                family = qs['family'][0]
        except:
                family = 'wiki'
	try:
		days = qs['days'][0]
	except:
		days = 100
else:
        lang = "cs"
        family = "wiki"
	days = 100

wiki = lang + family
conn = db.connect(wiki)

d = datetime.today() - timedelta(days=int(days))

print 'Content-type: text/html\n'
print """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Statistika patrolářů v """ + wiki + """</title>
        </head>
        <body>
"""

cur = conn.cursor()
with cur:
	sql = 'select count(*), log_user_text from logging where log_type="patrol" and log_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) +'" group by log_user order by count(*) desc;'
	cur.execute(sql)
	data = cur.fetchall()

print HTML.table(data)

print """
</body>
</html>
"""
