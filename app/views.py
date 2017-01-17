from flask import render_template, request, flash, url_for, redirect
from app import app
from .forms import AccountCreationForm
from flask_wtf.csrf import CsrfProtect


CsrfProtect(app)


''''
@csrf.error_handler
def csrf_error(reason):
	return render_template('csrf_error.html', reason=reason), 400
'''


@app.route('/')
@app.route('/index')
@app.route('/search')
def search():
	return render_template("search.html")


@app.route('/about')
def about():
	return render_template("about.html")


@app.route('/account', methods=['GET', 'POST'])
def account():
	form = AccountCreationForm()
	if form.validate_on_submit():
		# Add User to DB.
		# Add Info to UtilDB
		flash("Thanks for registering")
		return redirect(url_for('search'))
	return render_template("account_creation.html", form=form)


@app.route('/properties', methods=['GET'])
def properties():
	search_string = request.args.get('search_string')
	return render_template("properties.html", search_string=search_string)


@app.route('/test', methods=['POST'])
def test():
	account_data = request.args.get('account_data')
	return render_template("test.html", account_data=account_data)
