"""The Design Lab server!"""
import os
import json
from time import time

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from instagram import client

from model import Style, Size, Waist, Fabric, Color, Embroidery, Stitching, connect_to_db, db


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ommmnamasteshantishantishanti" 

app.jinja_env.undefined = StrictUndefined
app.jinja_env.globals.update(time=time)

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

	session['current_design'] = {
		"style_id": None,
		"style_svg": "model.svg",
		"size_code": None,
		"waist_id": None,
		"fabric_id": None,
		"color_id": None,
		"color_hex": None,
		"embroidery_text": None,
		"embroidery_place":None,
		"stitching_style": None
		}
	return render_template("landing_page.html")


@app.route('/step1')
def step_one():
	"""Form to choose style, size, cut, waist"""

	styles = Style.query.filter(Style.discontinued == False).order_by(Style.style_id).all()
	sizes = Size.query.filter(Size.discontinued == False).all()
	waists = Waist.query.filter(Waist.discontinued == False).order_by(Waist.waist_id).all()
	
	
	return render_template("step1.html", styles=styles, sizes=sizes, waists=waists)


@app.route('/current-design.json')
def current_design():
	"""JSON information about the current user's design"""

	return jsonify(session['current_design'])


@app.route('/styles.json')
def styles():
	"""Returns style options from db via JSON"""

	styles = db.session.query(Style.style_svg, Style.style_id).all()

	return jsonify({"styles": styles})


@app.route('/step2', methods=["POST"])
def step_two():
	"""Form to choose fabric"""


	session['current_design']['style_id'] = request.form.get('style')
	session['current_design']['size_code'] = request.form.get('size')
	session['current_design']['style_svg'] = request.form.get('style-svg')
	session['current_design']['waist_id'] = request.form.get('waist')
	

	fabrics = Fabric.query.filter(Fabric.discontinued == False).all()
	return render_template("step2.html", fabrics=fabrics)


@app.route('/step3', methods=["POST"])
def step_three():
	"""Last form: choose fabric color and custom embroidery"""

	session['current_design']['fabric_id'] = request.form.get('fabric')
	fab_id = session['current_design']['fabric_id']

	colors = Color.query.filter(Color.fabric_id==fab_id).all()
	embroidery = Embroidery.query.filter(Embroidery.discontinued == False).all()
	stitch = Stitching.query.filter(Stitching.discontinued == False).all()

	return render_template("step3.html", colors=colors, embroidery=embroidery, stitch=stitch)



@app.route('/myDesignLab', methods=["GET", "POST"])
def my_design():
	"""Display the finished design with options to save or purchase"""

	session['current_design']['color_id'] = request.form.get('color')
	session['current_design']['color_hex'] = request.form.get('hex')
	session['current_design']['embroidery_text'] = request.form.get('embroidery')
	session['current_design']['embroidery_place'] = request.form.get('emb-place')
	session['current_design']['stitching_style'] = request.form.get('stitch')

	print "\n\n\n"
	print session['current_design']  
	print "\n\n\n"

	return render_template("myDesignLab.html")

@app.route('/newDesign')
def new():

	session['current_design'] = {
		"style_id": None,
		"style_svg": "model.svg",
		"size_code": None,
		"waist_id": None,
		"fabric_id": None,
		"color_id": None,
		"color_hex":None,
		"embroidery_text": None,
		"embroidery_place": None,
		"stitching_style": None
		}

	return redirect('/step1')

@app.route('/selections.json')
def selections():
	"""Returns design details from db via JSON"""

	style_sesh = session['current_design']['style_id']
	style = db.session.query(Style.style_name).filter(Style.style_id==style_sesh).one()
	
	size_sesh = session['current_design']['size_code']
	size = db.session.query(Size.size).filter(Size.size_code==size_sesh).one()

	# waist_sesh = session['current_design']['waist_id']
	# waist = db.session.query(Waist.waist_name).filter(Waist.waist_id==waist_sesh).one()

	fab_sesh = session['current_design']['fabric_id']
	fabric = db.session.query(Fabric.fabric_name).filter(Fabric.fabric_id==fab_sesh).one()

	color_sesh = session['current_design']['color_id']
	color = db.session.query(Color.color_name).filter(Color.color_id==color_sesh).one()

	place_sesh = session['current_design']['embroidery_place']
	# placement = db.session.query(Embroidery.embroidery_location).filter(Embroidery.embroidery_id==place_sesh).one()
	stitch_sesh = session['current_design']['stitching_style']
	text_sesh = session['current_design']['embroidery_text']

	return jsonify({"selections": {"style": style[0], 
								   "size": size[0],
								   # "waist":waist[0],
								   "fabric":fabric[0],
								   "color":color[0],
								   "placement": place_sesh,
								   "stitch": stitch_sesh,
								   "text": text_sesh
								   }
					})


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

	tagged_media, next = api.tag_recent_media(count=60, tag_name='superfoodoffashion')
	print tagged_media
	for n in tagged_media:
		print n


	lookbookData = {
			'our_media' : our_recent_media,
			'tagged' : tagged_media
	}

	print lookbookData

	return render_template('lookbook.html', **lookbookData )
	


##################################################

if __name__ == "__main__":
    
    app.debug = True #Switch to False when demo/deploying!!!!

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    print "\n\n\nYO\n\n\n"
    app.run()