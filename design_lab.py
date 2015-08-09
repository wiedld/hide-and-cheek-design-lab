"""The Design Lab server!"""
import os
import json

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from instagram import client

from model import Style, Size, Cut, Waist, Fabric, Color, connect_to_db, db


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ommmnamasteshantishantishanti" 

app.jinja_env.undefined = StrictUndefined

#configure the Instagram API
instaConfig = {
	'client_id':os.environ.get('INSTAGRAM_CLIENT_ID'),
	'client_secret':os.environ.get('INSTAGRAM_CLIENT_SECRET'),
	'redirect_uri':os.environ.get('REDIRECT_URI')	
}

api = client.InstagramAPI(**instaConfig)

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
		"embroidery_place":None
		}


	fabrics = Fabric.query.filter(Fabric.discontinued == False).all()
	return render_template("step2.html", fabrics=fabrics)


@app.route('/step3', methods=["POST"])
def step_three():
	"""Last form: choose fabric color"""

	session['current_design']['fabric_id'] = request.form.get('fabric')
	fab_id = session['current_design']['fabric_id']

	colors = Color.query.filter(Color.fabric_id==fab_id).all()
	return render_template("step3.html", colors=colors)



@app.route('/myDesignLab', methods=["GET", "POST"])
def myLab():
	"""Display the finished design with options to save or purchase"""

	session['current_design']['color_id'] = request.form.get('color')
	session['current_design']['embroidery'] = request.form.get('embroidery')
	session['current_design']['embroidery_place'] = request.form.get('emb-place')

	print "\n\n\n"
	print session['current_design']  
	print "\n\n\n"

	return render_template("myDesignLab.html")

#FIXME
@app.route('/saved', methods=["POST"])
def save():
	"""Saves the current design to the database"""

	style_id = session['current_design']['style_id']
	
	new_design = Design(style_id=style_id,  ) #FIXME

	flash("Your design is saved!")
	return redirect('/myDesignLab')





@app.route('/Lookbook', methods=["GET", "POST"])
def lookbook():
	"""Display most-recent Instagram images with the hideandcheek hashtag""" #FIXME : make this the *most-liked* insta images, not just the most recent



	our_recent_media, next = api.user_recent_media(user_id="1558910306", count=10)
	for media in our_recent_media:
		print media

	print "\n\n\n\n"

	tagged_media, next = api.tag_recent_media(tag_name='superfoodoffashion')
	print tagged_media
	for n in tagged_media:
		print n


	lookbookData = {
			'our_media' : our_recent_media,
			'tagged' : tagged_media
	}

	print lookbookData

	return render_template('lookbook.html', **lookbookData )
	


	# if 'access_token' not in session:
	# 	flash('Ooops! We are having problems loading data from instagram. Please check back later! \nxo \n-h&c team')
 #        return redirect('/')

    


##################################################

if __name__ == "__main__":
    
    app.debug = True #Switch to False when demo/deploying!!!!

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    print "\n\n\nYO\n\n\n"
    app.run()