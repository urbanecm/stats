#!/usr/bin/env python
#-*- coding: utf-8 -*-

import HTML
from datetime import datetime, timedelta
from wmflabs import db
conn = db.connect('cswiki')

d = datetime.today() - timedelta(days=100)

cur = conn.cursor()
with cur:
	sql = 'select count(*), log_user_text from logging where log_type="patrol" and log_action="patrol" and log_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) +'" group by log_user order by count(*) desc;'
	cur.execute(sql)
	data = cur.fetchall()

print HTML.table(data)
