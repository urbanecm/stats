# -*- coding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import flask
from flask import request
import HTML
from datetime import datetime, timedelta
from wmflabs import db

app = flask.Flask(__name__)

@app.route('/')
def index():
	return flask.render_template('index.html')

@app.route('/edit')
def edit():
	wiki = request.args.get('wiki')
	if wiki == None:
		wiki = "cswiki"
	conn = db.connect(wiki)
	cur = conn.cursor()
	with cur:
		d = datetime.today() - timedelta(days=days)
		sql = 'select count(*), rev_user_text from revision where rev_timestamp>="' + '{:%Y%m%d%H%M%S}'.format(d) + '" and rev_user not in (select ug_user from user_groups where ug_group="bot") group by rev_user_text order by count(*) desc;'
		cur.execute(sql)
		data = cur.fetchall()
	return flask.render_template('edit.html', table=HTML.table(data))
