"""Models and database functions for DesignLab"""

from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

######################################
#Model Definitions: Style/Size/Cut/Waist/Fabric/Color/Design/Order

class Style(db.Model):
	"""Style options"""

	__tablename__ = "styles"

	style_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	style_name = db.Column(db.String(50), nullable=False)
	style_description = db.Column(db.String(200), nullable=False)
	img_layer = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Style: style_id = %s style_name = %s>" % (self.style_id, self.style_name)


class Size(db.Model):
	"""Size options"""

	__tablename__ = "sizes"

	size_code = db.Column(db.String(2), autoincrement=True, primary_key=True)
	size = db.Column(db.String(20), nullable=False)
	size_description = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Size: size_code = %s>" % self.size_code


class Cut(db.Model):
	"""Crop length options"""

	__tablename__ = "cuts"

	cut_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	cut_name = db.Column(db.String(50), nullable=False)
	cut_css = db.Column(db.String(50), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Cut: cut_id = %s cut = %s>" % (self.cut_id, self.cut_name)


class Waist(db.Model):
	"""Waist height options"""

	__tablename__ = "waists"

	waist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	waist_name = db.Column(db.String(50), nullable=False)
	waist_description = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Waist: waist_id = %s waist_name = %s>" % (self.waist_id, self.waist_name)


class Fabric(db.Model):
	"""Fabric options"""

	__tablename__ = "fabrics"

	fabric_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	fabric_name = db.Column(db.String(50), nullable=False)
	fabric_description = db.Column(db.String(800), nullable=False)
	fabric_thumbnail = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	def __repr__(self):
		"""Quick reference when the object is printed"""
		return "<Fabric: fabric_id = %s fabric_name = %s >" % (self.fabric_id, self.fabric_name)


class Color(db.Model):
	"""Color options for each fabric"""
	__tablename__ = "colors"

	color_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	color_name = db.Column(db.String(50), nullable=False)
	fabric_id = db.Column(db.Integer, db.ForeignKey('fabrics.fabric_id'), nullable=False)
	color_rgb = db.Column(db.String(20), nullable=False)
	color_thumbnail = db.Column(db.String(200), nullable=False)
	discontinued = db.Column(db.Boolean, default=False, nullable=False)

	#Defines relationship to the Fabric class
	fabric = db.relationship("Fabric", backref=db.backref("colors"))

	def __repr__(self):
		"""Quick reference when printed"""
		return "<Color: color_id = %s color_name = %s fabric_id = %s>" % (self.color_id, self.color_name, self.fabric_id)


class Design(db.Model):
	"""User generated designs"""
	__tablename__ = "designs"

	design_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	style_id = db.Column(db.Integer, db.ForeignKey('styles.style_id'), nullable=False)
	size_code = db.Column(db.String(2), db.ForeignKey('sizes.size_code'), nullable=False)
	cut_id = db.Column(db.Integer, db.ForeignKey('cuts.cut_id'), nullable=False)
	waist_id = db.Column(db.Integer, db.ForeignKey('waists.waist_id'), nullable=False)
	fabric_id = db.Column(db.Integer, db.ForeignKey('fabrics.fabric_id'), nullable=False)
	color_id = db.Column(db.Integer, db.ForeignKey('colors.color_id'), nullable=False)

	#Defines class relationships
	style = db.relationship("Style", backref=db.backref("designs"))
	size = db.relationship("Size", backref=db.backref("designs"))
	cut = db.relationship("Cut", backref=db.backref("designs"))
	waist = db.relationship("Waist", backref=db.backref("designs"))
	fabric = db.relationship("Fabric", backref=db.backref("designs"))
	color = db.relationship("Color", backref=db.backref("designs"))


class Order(db.Model):
	"""Order information for fulfillment portal"""
	__tablename__ = "orders"

	order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	design_id = db.Column(db.Integer, db.ForeignKey('designs.design_id'), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	address = db.Column(db.String(800), nullable=False)
	state = db.Column(db.String(10), nullable=False)
	zipcode = db.Column(db.Integer, nullable=False)

	design = db.relationship("Design", backref=db.backref("orders"))

# class Measurement(db.Model):
# 	"""Design-specific sizing and measurement information"""
# 	__tablename__ = "measurements"


#######################################
#Helper functions

def connect_to_db(app):
	"""Connects db to flask app."""

	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///designlab.db'
	db.app = app
	db.init_app(app)

if __name__ == '__main__':
	#Enables running this module interactively to interact directly w/ the database.

	from design_lab import app
	connect_to_db(app)
	print "Connected to DesignLab DB."
