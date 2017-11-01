from bookapp import app
from flask import render_template

@app.route('/home')
def index():
	return render_template('base.html')
