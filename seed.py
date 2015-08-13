"""File to seed design database from raw data in seed_data/"""

from model import Style, Size, Waist, Fabric, Color, Embroidery, Stitching, connect_to_db, db

from design_lab import app


def load_styles(file_name):
	"""Loads syle info from raw.styles into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		style_name = row[0]
		style_description = row[1]
		style_svg = row[2]
		discontinued = row[3]

		style = Style(style_name=style_name, style_description=style_description, style_svg=style_svg, discontinued=discontinued)

		db.session.add(style)
	db.session.commit()


def load_sizes(file_name):
	"""Loads syle info from raw.sizes into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		size_code = row[0]
		size = row[1]
		size_description = row[2]

		size = Size(size_code=size_code, size=size, size_description=size_description)

		db.session.add(size)
	db.session.commit()


def load_waists(file_name):
	"""Loads waist height info from raw.waists into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		waist_name = row[0]
		waist_description = row[1]

		waist = Waist(waist_name=waist_name, waist_description=waist_description)

		db.session.add(waist)
	db.session.commit()


def load_fabrics(file_name):
	"""Loads fabric information from raw.fabrics into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		fabric_name = row[0]
		fabric_description = row[1]
		fabric_thumbnail = row[2]
		discontinued = row[3]

		fabric = Fabric(fabric_name=fabric_name, fabric_description=fabric_description, fabric_thumbnail=fabric_thumbnail, discontinued=discontinued)

		db.session.add(fabric)
	db.session.commit()


def load_colors(file_name):
	"""Loads color information from raw.colors into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		color_name = row[0]
		color_hex = row[1]
		color_thumbnail = row[2]
		fabric_id = row[3]

		color = Color(color_name=color_name, color_hex=color_hex, color_thumbnail=color_thumbnail, fabric_id=fabric_id)

		db.session.add(color)
	db.session.commit()

def load_embroidery(file_name):
	"""Loads embroidery information from raw.embroidery into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		embroidery_location = row[0]

		embroidery = Embroidery(embroidery_location=embroidery_location)

		db.session.add(embroidery)
	db.session.commit()

def load_stitching(file_name):
	"""Loads stitching information from raw.stitching into the database"""

	raw_data = open(file_name)

	for line in raw_data:
		row = line.rstrip().lstrip().split("|")
		stitching_style = row[0]
		thumbnail = row[1]

		stitching = Stitching(stitching_style=stitching_style, thumbnail=thumbnail)

		db.session.add(stitching)
	db.session.commit()
#################################

if __name__ == "__main__":
	connect_to_db(app)

	load_styles("seed_data/raw.styles")
	load_sizes("seed_data/raw.sizes")
	load_waists("seed_data/raw.waists")
	load_fabrics("seed_data/raw.fabrics")
	load_colors("seed_data/raw.colors")
	load_embroidery("seed_data/raw.embroidery")
	load_stitching("seed_data/raw.stitching")

