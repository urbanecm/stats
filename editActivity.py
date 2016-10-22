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
else:
        lang = "cs"
        family = "wiki"

wiki = lang + family
conn = db.connect(wiki)

d = datetime.today() - timedelta(days=100)

print 'Content-type: text/html\n'
print """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Statistika editací v """ + wiki + """</title>
        </head>
        <body>
"""

cur = conn.cursor()
with cur:
	sql = 'select count(*), rev_user_text from revision where rev_timestamp>="20160701000000" and rev_user not in (select ug_user from user_groups where ug_group="bot") group by rev_user order by count(*) desc;'
	cur.execute(sql)
	data = cur.fetchall()

print HTML.table(data)

print """
</body>
</html>
"""
