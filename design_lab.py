"""The Design Lab server!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Style, Size, Cut, Waist, Fabric, Color, connect_to_db, db


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC" 


app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
	"""Landing page"""
	return render_template("landing_page.html")

@app.route('/step1')
def step_one():
	"""Form to choose style, size, cut, waist"""

	styles = Style.query.order_by(Style.style_name).all()
	sizes = Size.query.all()
	cuts = Cut.query.order_by(Cut.cut_id).all()
	waists = Waist.query.order_by(Waist.waist_id).all()


	return render_template("step1.html", styles=styles, sizes=sizes, cuts=cuts, waists=waists)






##################################################

if __name__ == "__main__":
    
    app.debug = True #Switch to False when demo/deploying!!!!

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    print "\n\n\nYO\n\n\n"
    app.run()