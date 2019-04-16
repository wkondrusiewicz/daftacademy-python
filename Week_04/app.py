# -*- coding: utf-8 -*-


from flask import Flask, jsonify, request, g, Response
import sqlite3
import json

app = Flask(__name__)

DATABASE = 'chinook.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/tracks', methods=['GET', 'POST'])
def tracks():
    db = get_db()
    if request.method == 'GET':
        art_name = request.args.get('artist', None)
        per_page = request.args.get('per_page', None)
        page = request.args.get('page', None)
        if art_name is not None:
            data = []
            temp = db.execute('SELECT albums.albumid FROM albums WHERE albums.artistid = (SELECT artists.artistid FROM artists WHERE artists.name = ?) ;',
                              (art_name,)).fetchall()
            for i in temp:
                data.append(db.execute(
                    'SELECT tracks.name FROM tracks WHERE tracks.albumid = ? ORDER BY name COLLATE NOCASE ASC;', (i[0],)).fetchall())
            data = [item for sublist in data for item in sublist]
            data = [item for sublist in data for item in sublist]
            data.sort()
            if per_page is not None:
                if page is not None:
                    beg = (int(page) - 1) * int(per_page)
                    end = (int(page)) * int(per_page)
                    data = data[beg:end]
                else:
                    end = int(per_page)
                    data = data[:end]
        else:
            data = db.execute(
                'SELECT name FROM tracks ORDER BY name COLLATE NOCASE ASC').fetchall()
            data = [item for sublist in data for item in sublist]
            if per_page is not None:
                if page is not None:
                    beg = (int(page) - 1) * int(per_page)
                    end = (int(page)) * int(per_page)
                    data = data[beg:end]
                else:
                    end = int(per_page)
                    data = data[:end]
        print(len(data))
        return Response(json.dumps(data),  mimetype='application/json')
    if request.method == 'POST':
        if not request.is_json:
            return 'Data is not json', 400
        content = request.get_json()
        keys = ["album_id", "media_type_id", "genre_id", "name",
                "composer", "milliseconds", "bytes", "price"]
        if all([k in list(content.keys()) for k in keys]) == False:
            return 'Missing required keys', 400
        db = get_db()
        lenght = len(db.execute('SELECT trackid FROM tracks').fetchall())
        keys2 = ["albumid", "mediatypeid", "genreid", "name",
                 "composer", "milliseconds", "bytes", "unitprice"]
        content2 = dict(zip(keys2, content.values()))
        content2['trackid'] = lenght + 1
        content['track_id'] = lenght + 1
        print(content2)
        try:
            db.execute(
                f'INSERT INTO tracks {tuple(content2.keys())} VALUES {tuple(content2.values())};')
            db.commit()
            return Response(json.dumps(content),  mimetype='application/json'), 200
        except:
            return 'Failed insertion into database', 400


@app.route('/genres', methods=['GET'])
def genres():
    db = get_db()
    data = db.execute('SELECT genreid FROM genres;').fetchall()
    names = db.execute('SELECT name FROM genres;').fetchall()
    names = [item for sublist in names for item in sublist]

    data = [item for sublist in data for item in sublist]
    data2 = []
    for i in data:
        data2.append(db.execute(
            'SELECT COUNT(*) FROM tracks WHERE tracks.genreid = ?', (i,)).fetchall())
    data2 = [item for sublist in data2 for item in sublist]
    data2 = [item for sublist in data2 for item in sublist]
    data3 = dict(zip(names, data2))
    print(names)
    return Response(json.dumps(data3),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
