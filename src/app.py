#!/usr/bin/env python3

from flask import Flask, render_template, request
from datetime import datetime, timedelta
import toolforge

app = Flask(__name__, static_folder='../static')

def decode_if_necessary(data):
	data_ = []
	for row in data:
		row_ = []
		for item in row:
			if isinstance(item, bytes):
				row_.append(item.decode('utf-8'))
			else:
				row_.append(item)
		data_.append(row_)
	return data_

@app.route('/')
def index():
	return 'a'

@app.route('/patrol')
def patrol():
	days = int(request.args.get('days', 100))
	lang = request.args.get('lang', 'cs')
	family = request.args.get('family', 'wikipedia')
	dbname = lang + family.replace('wikipedia', 'wiki')
	conn = toolforge.connect(dbname)
	d = datetime.today() - timedelta(days=int(days))

	cur = conn.cursor()
	with cur:
		sql = 'select count(*), actor_name from logging join actor on actor_id=log_actor where log_type="patrol" and log_action="patrol" and log_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) +'" group by log_actor order by count(*) desc;'
		cur.execute(sql)
		data = decode_if_necessary(cur.fetchall())
	cur = conn.cursor()
	with cur:
		sql = 'select count(*) from logging where log_type="patrol" and log_action="patrol" and log_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) +'";'
		cur.execute(sql)
		data.append((cur.fetchall()[0][0], "<strong>Celkem</strong>"))
	
	return render_template('data.html', data=data, days=days, wiki=dbname, what="patrolářů")

@app.route('/rollback')
def rollback():
	days = int(request.args.get('days', 100))
	lang = request.args.get('lang', 'cs')
	family = request.args.get('family', 'wikipedia')
	dbname = lang + family.replace('wikipedia', 'wiki')
	conn = toolforge.connect(dbname)
	d = datetime.today() - timedelta(days=int(days))

	with conn.cursor() as cur:
		cur.execute('select ctd_id from change_tag_def where ctd_name="mw-rollback"')
		tmp = cur.fetchall()
		ctd_id = tmp[0][0]

	cur = conn.cursor()
	with cur:
		sql = 'select count(*), actor_name from change_tag join revision on rev_id=ct_rev_id join actor_revision on rev_actor=actor_id where ct_tag_id=%d and rev_timestamp >= "%s" group by rev_actor order by count(*) desc;' % (ctd_id, '{:%Y%m%d%H%M%S}'.format(d))
		cur.execute(sql)
		data = decode_if_necessary(cur.fetchall())

	return render_template('data.html', data=data, days=days, wiki=dbname, what="revertérů")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
