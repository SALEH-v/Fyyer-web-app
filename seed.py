# # THIS IS A SEED SCRIPT TO INSERT ALL RQUIRED DATA IN DATABASE


# # from models import *
# # from app import *

# # db = SQLAlchemy(app)

# def create_venus():
#     venues = [{
#         "id" : 1,
#         "name": "The Musical Hop",
#         "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
#         "address": "1015 Folsom Street",
#         "city": "San Francisco",
#         "state": "CA",
#         "phone": "123-123-1234",
#         "website": "https://www.themusicalhop.com",
#         "facebook_link": "https://www.facebook.com/TheMusicalHop",
#         "seeking_talent": True,
#         "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
#         "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
#     }, {
#         "id" :2,
#         "name": "The Dueling Pianos Bar",
#         "genres": ["Classical", "R&B", "Hip-Hop"],
#         "address": "335 Delancey Street",
#         "city": "New York",
#         "state": "NY",
#         "phone": "914-003-1132",
#         "website": "https://www.theduelingpianos.com",
#         "facebook_link": "https://www.facebook.com/theduelingpianos",
#         "seeking_talent": False,
#         "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"
#     }, {
#         "id" :3,
#         "name": "Park Square Live Music & Coffee",
#         "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
#         "address": "34 Whiskey Moore Ave",
#         "city": "San Francisco",
#         "state": "CA",
#         "phone": "415-000-1234",
#         "website": "https://www.parksquarelivemusicandcoffee.com",
#         "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
#         "seeking_talent": False,
#         "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
#     }]

#     for venue in venues:
#         new_venue = Venue()
#         for key in venue.keys():
#             setattr(new_venue, key, venue[key])
#         db.session.add(new_venue)
#         db.session.commit()


# def create_artists():
#     artists = [{
#         "id" :4,
#         "name": "Guns N Petals",
#         "genres": ["Rock n Roll"],
#         "city": "San Francisco",
#         "state": "CA",
#         "phone": "326-123-5000",
#         "website": "https://www.gunsnpetalsband.com",
#         "facebook_link": "https://www.facebook.com/GunsNPetals",
#         "seeking_venue": True,
#         "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
#         "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     }, {
#         "id":5,
#         "name": "Matt Quevedo",
#         "genres": ["Jazz"],
#         "city": "New York",
#         "state": "NY",
#         "phone": "300-400-5000",
#         "facebook_link": "https://www.facebook.com/mattquevedo923251523",
#         "seeking_venue": False,
#         "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
#     }, {
#         "id" :6,
#         "name": "The Wild Sax Band",
#         "genres": ["Jazz", "Classical"],
#         "city": "San Francisco",
#         "state": "CA",
#         "phone": "432-325-5432",
#         "seeking_venue": False,
#         "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
#     }]

#     for artist in artists:
#         new_artist = Artist()
#         for key in artist.keys():
#             setattr(new_artist, key, artist[key])
#         db.session.add(new_artist)
#         db.session.commit()


# def create_shows():
#     shows = [{
#         "venue_id": db.session.query(Venue).filter_by(name="The Musical Hop").first().id,
#         "artist_id": db.session.query(Artist).filter_by(name="Guns N Petals").first().id,
#         "start_time": "2019-05-21T21:30:00.000Z"
#     }, {
#         "venue_id": db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
#         "artist_id": db.session.query(Artist).filter_by(name="Matt Quevedo").first().id,
#         "start_time": "2019-06-15T23:00:00.000Z"
#     }, {
#         "venue_id": db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
#         "artist_id": db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
#         "start_time": "2035-04-01T20:00:00.000Z"
#     }, {
#         "venue_id": db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
#         "artist_id": db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
#         "start_time": "2035-04-08T20:00:00.000Z"
#     }, {
#         "venue_id": db.session.query(Venue).filter_by(name="Park Square Live Music & Coffee").first().id,
#         "artist_id": db.session.query(Artist).filter_by(name="The Wild Sax Band").first().id,
#         "start_time": "2035-04-15T20:00:00.000Z"
#     }]

#     for show in shows:
#         new_show = Show()
#         for key in show.keys():
#             setattr(new_show, key, show[key])
#         db.session.add(new_show)
#         db.session.commit()


# def clear_data(session):
#     meta = db.metadata
#     for table in reversed(meta.sorted_tables):
#         print('Clear table %s' % table)
#         session.execute(table.delete())
#     session.commit()


# clear_data(db.session)

# create_venus()
# create_artists()
# create_shows()
