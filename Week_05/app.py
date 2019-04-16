import os

from flask import Flask, abort, render_template, request, Response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, update

import models
import json
from models import Base


DATABASE_URL = os.environ['DATABASE_URL']

# engine = create_engine("postgresql://new2:new2@localhost:5432/chinook")
engine = create_engine(DATABASE_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()



@app.route("/counter", methods=["GET"])
def counter():
    if request.method == "GET":

        counter_value=(db_session.query(models.Counter)
        .filter(models.Counter.wejscia=='licznik')
        .first()
                       )
        print(counter_value.ile_razy)
        counter_value.ile_razy=counter_value.ile_razy+1
        db_session.commit()

        actual_value = db_session.query(models.Counter).all()
        return str(actual_value[1].ile_razy)

@app.route("/counter_create", methods=["GET"])
def counter_create():
    if request.method == "GET":
        try:

            meta = MetaData()

            students = Table(
                'counter', meta,
                Column('wejscia', String, primary_key=True),
                Column('ile_razy', Integer)
            )
            meta.create_all(engine)
            newArist = models.Counter(wejscia='licznik2', ile_razy=2)
            db_session.add(newArist)
            db_session.commit()
            newArist = models.Counter(wejscia='licznik', ile_razy=0)
            db_session.add(newArist)
            db_session.commit()
        except:
            pass
        return "ok"



@app.route("/counter_reset", methods=["GET"])
def counter_reset():
    if request.method == "GET":
        counter_value=(db_session.query(models.Counter)
        .filter(models.Counter.wejscia=='licznik')
        .first()
                       )
        print(counter_value.ile_razy)
        counter_value.ile_razy=0
        db_session.commit()
        return "ok"




# @app.route("/longest_tracks", methods=["GET"])
# def longest_tracks():
#     if request.method == "GET":
#         tracks = db_session.query(models.Track).order_by(models.Track.milliseconds.desc()).limit(10).all()
#         list_dicts = []
#         for x in tracks:
#             y = x.__dict__
#             y.pop('_sa_instance_state')
#             for k,v in y.items():
#                 y[k] = str(v)
#             #y['unit_price'] = str(y['unit_price'])
#             #y['name'] = y['name'].encode('ascii', 'ignore')
#             list_dicts.append(y)
#             #print(y, len(y))
#         list_dicts.sort(key=lambda x: x['milliseconds'],reverse=True)
#         return jsonify(list_dicts)


@app.route("/longest_tracks_by_artist", methods=["GET"])
def longest_tracks_by_artist():
    if request.method == "GET":
        list_dicts = []
        art_name = request.args.get('artist', None)
        if art_name is not None:
            if len(art_name)==0:
                print('Please pass something in the query string')
                abort(404)
            art_id= db_session.query(models.Artist).filter(models.Artist.name==art_name).all()
            for x in art_id:
                alb_id = db_session.query(models.Album).filter(models.Album.artist_id==x.artist_id).all()
                for y in alb_id:
                    tracks = db_session.query(models.Track).filter(models.Track.album_id==y.album_id).order_by(models.Track.milliseconds.desc()).all()
                    for x in tracks:
                        y = x.__dict__
                        y.pop('_sa_instance_state')
                        for k,v in y.items():
                            y[k] = str(v)
                        #y['unit_price'] = str(y['unit_price'])
                        list_dicts.append(y)
            if len(list_dicts)==0:
                print('Artist not found in the database')
                abort(404)
            list_dicts.sort(key=lambda x: x['milliseconds'],reverse=True)
            list_dicts = list_dicts[:10]
            return jsonify(list_dicts)
        else:
            print('Please use query string with artist=SOME_NAME')
            abort(404)


@app.route("/count_songs", methods=["GET"])
def count_songs():
    if request.method == "GET":
        art_name = request.args.get('artist', None)
        song_count = []
        if art_name is not None:
            art_name = art_name.split(',')
            for nm in art_name:
                counter = 0
                art_id= db_session.query(models.Artist).filter(models.Artist.name==nm).all()
                for x in art_id:
                    alb_id = db_session.query(models.Album).filter(models.Album.artist_id==x.artist_id).all()
                    for y in alb_id:
                        tracks = db_session.query(models.Track).filter(models.Track.album_id==y.album_id).count()
                        counter +=tracks
                        print(counter)
                song_count.append(counter)
                if counter==0:
                    abort(404)
            data = dict(zip(art_name,song_count))

            return jsonify(data)
        else:
            abort(404)



@app.route("/artists", methods=["POST"])
def artists():
    if request.method == "POST":
        if not request.is_json:
            return 'Data is not json', 400
        content = request.get_json()
        if 'name' not in content.keys():
            return 'Invalid keys', 400
        if len(content) != 1:
            return 'There should only be one key', 400

        old_id = db_session.query(models.Artist).count()
        new_name = content.get('name')
        print(old_id)
        try:
            newArist = models.Artist(artist_id=old_id+1, name=new_name)
            db_session.add(newArist)
            db_session.commit()
            return jsonify(dict(zip(['artist_id','name'],[str(old_id),str(new_name)])))
        except:
            abort(400)




if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)
