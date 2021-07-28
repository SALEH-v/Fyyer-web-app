from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)

    venue_id = db.Column(
        db.Integer,
        db.ForeignKey('Venue.id'))

    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('Artist.id'))

    start_time = db.Column(db.DateTime)

    venue = db.relationship("Venue", backref=db.backref("Show", cascade="all, delete-orphan"))
    artist = db.relationship("Artist", backref=db.backref("Show", cascade="all, delete-orphan"))


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    genres = db.Column(db.String())
    website = db.Column(db.String(500))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    shows = db.relationship('Show', backref='Venue', lazy=True)

    # shows = db.relationship("Show", backref=db.backref('Venue', lazy=True), overlaps="venue")

    # Artists = db.relationship('Artist', secondary=Show, backref=db.backref('Venue', lazy=True))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    image_link = db.Column(db.String(500))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    shows = db.relationship("Show", backref=db.backref('Artist', lazy=True))


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


    # TODO: implement any missing fields, as a database migration using Flask-Migrate


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
