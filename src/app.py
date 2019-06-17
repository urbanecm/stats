#!/usr/bin/env python3

from flask import Flask, render_template, request
from datetime import datetime, timedelta
import toolforge

app = Flask(__name__, static_folder='../static')

def decode_if_necessary(data):
	for row in rows:
		row_ = []
		for item in row:
			if isinstance(item, bytes):
				row_.append(item.decode('utf-8'))
			else:
				row_.append(item)
	return date

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

	data = []
	cur = conn.cursor()
	with cur:
		sql = 'select count(*), actor_name from logging join actor on actor_id=log_actor where log_type="patrol" and log_action="patrol" and log_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) +'" group by log_actor order by count(*) desc;'
		cur.execute(sql)
		rows = decode_if_necessary(cur.fetchall())
	cur = conn.cursor()
	with cur:
		sql = 'select count(*) from logging where log_type="patrol" and log_action="patrol" and log_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) +'";'
		cur.execute(sql)
		rows = (cur.fetchall()[0][0], "<strong>Celkem</strong>")
	
	return render_template('data.html', data=data, days=days, wiki=dbname)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
