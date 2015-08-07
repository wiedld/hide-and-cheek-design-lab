"""The Design Lab server!"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
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

	styles = Style.query.filter(Style.discontinued == False).order_by(Style.style_name).all()
	sizes = Size.query.filter(Size.discontinued == False).all()
	cuts = Cut.query.filter(Cut.discontinued == False).order_by(Cut.cut_id).all()
	waists = Waist.query.filter(Waist.discontinued == False).order_by(Waist.waist_id).all()
	# need to filter these by discontinued isnot None
	
	return render_template("step1.html", styles=styles, sizes=sizes, cuts=cuts, waists=waists)


@app.route('/current-design.json')
def this_design():
	"""JSON information about the current user's design"""

	return jsonify(session['current_design'])



@app.route('/step2', methods=["POST"])
def step_two():
	"""Form to choose fabric"""


	cut_css = request.form.get('cut-css')
	cut = Cut.query.filter(Cut.cut_css == cut_css).one()
	cut_id = cut.cut_id


	session['current_design'] = {
		"style_id": request.form.get('style'),
		"img_layer": request.form.get('img-layer'),
		"size_code": request.form.get('size'),
		"cut_css": request.form.get('cut-css'),
		"cut_id": cut.cut_id,
		"waist_id": None,
		"fabric_id": None,
		"color_id": None,
		"embroidery": None,
		}


	fabrics = Fabric.query.filter(Fabric.discontinued == False).all()
	return render_template("step2.html", fabrics=fabrics)


@app.route('/step3', methods=["POST"])
def step_three():
	"""Last form: choose fabric color"""

	pass

@app.route('/myDesignLab', methods=["POST"])
def myLab():
	"""Display the finished design with options to save or purchase"""

	pass

@app.route('/Lookbook', methods=["GET", "POST"])
def lookbook():
	"""Display most-liked Instagram images with the hideandcheek hashtag"""

	pass




##################################################

if __name__ == "__main__":
    
    app.debug = True #Switch to False when demo/deploying!!!!

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    print "\n\n\nYO\n\n\n"
    app.run()