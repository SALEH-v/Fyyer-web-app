#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_migrate import Migrate, migrate
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import os
from flask_sqlalchemy import SQLAlchemy

from models import Artist, Venue, Show,db
from config import SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# TODO: connect to a local postgresql database

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SECRET_KEY = os.urandom(32)
# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = SECRET_KEY

moment = Moment(app)

db.init_app(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

#models.py




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
      
  # venues = db.session.query(Venue).all()

  data = []

  distVenues = db.session.query(Venue.city, Venue.state).distinct(Venue.city, Venue.state) 
  for v in distVenues:
      cityVen =  db.session.query(Venue.id, Venue.name).filter(Venue.city == v[0]).filter(Venue.state == v[1])
      data.append({"city": v[0],"state": v[1],"venues": cityVen})

     
  return render_template('pages/venues.html', areas=data);




@app.route('/venues/search', methods=['POST'])
def search_venues():


  search_term = request.form.get('search_term', '')
  data = db.session.query(Venue).filter(Venue.name.ilike("%{search_term}%".format(search_term=search_term))).all()

  response = {
    "count": len(data),
    "data": data
  }




  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))



 






@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
 

  data = {}

  venue = Venue.query.get(venue_id)

  past_shows = db.session.query(Show, Artist).filter(Show.venue_id == venue_id).filter(
      Show.start_time < datetime.now()).outerjoin(Show).all()

  upcoming_shows = db.session.query(Show, Artist).filter(Show.venue_id == venue_id).filter(
      Show.start_time > datetime.now()).outerjoin(Show).all()


  data['id'] = venue.id
  data['name'] = venue.name
  data['genres'] = venue.genres.replace("{", "").replace("}", "").replace('"', "").split(",")
  data['address'] = venue.address
  data['city'] = venue.city
  data['state'] = venue.state
  data['phone'] = venue.phone
  data['website'] = venue.website
  data['facebook_link'] = venue.facebook_link
  data['seeking_talent'] = venue.seeking_talent
  data['seeking_description'] = venue.seeking_description
  data['image_link'] = venue.image_link
  data['past_shows'] = list()
  data['upcoming_shows'] = list()
  for past_show in past_shows:
      data['past_shows'].append({
          "artist_id": past_show.Artist.id,
          "artist_name": past_show.Artist.name,
          "artist_image_link": past_show.Artist.image_link,
          "start_time": past_show.Show.start_time
      })

  for upcoming_show in upcoming_shows:
      data['upcoming_shows'].append({
          "artist_id": upcoming_show.Artist.id,
          "artist_name": upcoming_show.Artist.name,
          "artist_image_link": upcoming_show.Artist.image_link,
          "start_time": upcoming_show.Show.start_time
      })
  data['past_shows_count'] = len(data['past_shows'])
  data['upcoming_shows_count'] = len(data['upcoming_shows'])




  




  
  return render_template('pages/show_venue.html', venue=data)





#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  error = False
  body = {}
  try:
    name = request.form['name']
    city = request.form['city']
    state =  request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form['genres']
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website_link']
    seeking_talent = False
    if "seeking_talent" in request.form:
          seeking_talent = True
    seeking_description = request.form['seeking_description']

    venue = Venue(name = name, city = city, state = state, address = address,
    phone = phone, genres= genres, facebook_link = facebook_link, image_link = image_link,
    website = website, seeking_talent = seeking_talent, seeking_description = seeking_description
    )

    db.session.add(venue)
    db.session.commit()

    body['name'] = venue.name
    body['city'] = venue.city
    body['state'] = venue.state
    body['address'] = venue.address
    body['phone'] = venue.phone
    body['genres'] = venue.genres
    body['facebook_link'] = venue.facebook_link
    body['image_link'] = venue.image_link
    body['website_link'] = venue.website
    body['seeking_talent'] = venue.seeking_talent
    body['seeking_description'] = venue.seeking_description
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed !')
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  if error:
    abort (500)
  else:
    jsonify(body)

  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()


  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term', '')
  data = db.session.query(Artist).filter(Artist.name.ilike("%{search_term}%".format(search_term=search_term))).all()

  response = {
    "count": len(data),
    "data": data
  }


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.get(artist_id)

  past_shows = list()
  upcoming_shows = list()

  for show in artist.Show:
    if show.start_time > datetime.now():
      upcoming_shows.append(show)
    else:
      past_shows.append(show)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.replace("{", "").replace("}", "").replace('"', "").split(","), # I faced a problem with displaying genres, and this is how I solved it
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }


  
  
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get(artist_id)
  values = request.form.get(artist_id)
  form = VenueForm(values)

  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

    try:
        newvenue = request.form

        name = newvenue['name']
        city = newvenue['city']
        state = newvenue['state']
        address = newvenue['address']
        phone = newvenue['phone']
        genres = newvenue['genres']
        facebook_link = newvenue['facebook_link']
        image_link = newvenue['image_link']
        website = newvenue['website_link']
        seeking_venue = False
        if "seeking_venue" in request.form:
            seeking_venue = True
        seeking_description = newvenue['seeking_description']

        venue = Venue.query.get(artist_id)

        venue.name = name
        venue.city = city
        venue.state = state
        venue.address = address
        venue.phone = phone
        venue.genres = genres
        venue.facebook_link = facebook_link
        venue.image_link = image_link
        venue.website = website
        venue.seeking_venue = seeking_venue
        venue.seeking_description = seeking_description

        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()


    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    values = request.form.get(venue_id)
    form = VenueForm(values)

    
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    try:
        newvenue = request.form

        name = newvenue['name']
        city = newvenue['city']
        state = newvenue['state']
        address = newvenue['address']
        phone = newvenue['phone']
        genres = newvenue['genres']
        facebook_link = newvenue['facebook_link']
        image_link = newvenue['image_link']
        website = newvenue['website_link']
        seeking_talent = False
        if "seeking_talent" in request.form:
            seeking_talent = True
        seeking_description = newvenue['seeking_description']

        venue = Venue.query.get(venue_id)

        venue.name = name
        venue.city = city
        venue.state = state
        venue.address = address
        venue.phone = phone
        venue.genres = genres
        venue.facebook_link = facebook_link
        venue.image_link = image_link
        venue.website = website
        venue.seeking_talent = seeking_talent
        venue.seeking_description = seeking_description

        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  body = {}

  print(request.form)

  try:
    name = request.form['name']
    city = request.form['city']
    state =  request.form['state']
    phone = request.form['phone']
    genres = request.form['genres']
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website = request.form['website_link']
    seeking_venue = False
    if "seeking_venue" in request.form:
          seeking_venue = True
    seeking_description = request.form['seeking_description']

    artist = Artist(name = name, city = city, state = state, 
    phone = phone, genres= genres, facebook_link = facebook_link, image_link = image_link,
    website = website, seeking_venue = seeking_venue, seeking_description = seeking_description
    )

    db.session.add(artist)
    db.session.commit()

    body['name'] = artist.name
    body['city'] = artist.city
    body['state'] = artist.state
    body['phone'] = artist.phone
    body['genres'] = artist.genres
    body['facebook_link'] = artist.facebook_link
    body['image_link'] = artist.image_link
    body['website_link'] = artist.website
    body['seeking_venue'] = artist.seeking_venue
    body['seeking_description'] = artist.seeking_description
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except Exception as e:
    print(e)
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed !')
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  if error:
    abort (500)
  else:
    jsonify(body)

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------



@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

    shows = db.session.query(Show).all()


    data = list()
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time
        })
  
  
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  body = {}
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Show(artist_id = artist_id, venue_id = venue_id, start_time = start_time)

    db.session.add(show)
    db.session.commit()

    body['artist_id'] = show.artist_id
    body['venue_id'] = show.venue_id
    body['start_time'] = show.start_time
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except Exception as e:
    print(e)
    flash('An error occurred. Show could not be listed')
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)