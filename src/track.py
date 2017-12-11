# -*- coding: utf-8 -*-
import sqlite3

class Track:
    def __init__(self, name, artist=None, Id=None, file_path=None, features=None):
        self.id = Id
        self.name = name
        self.artist = artist
        self.file_path = file_path
        self.features = features
    
    def feature(self, feat_name, default=None):
        return self.features.get(feat_name, default)

    def __unicode__(self):
        return u"song %d: %s by %s at %s" % (self.id, self.name, self.artist, self.file_path)

    def __repr__(self):
        return self.__unicode__().encode('utf-8')


class TrackRepo:
    def __init__(self):
        raise NotImplementedError("This class cannot be used separately")
    
    def get_random_tracks(self, count, feature_constraints):
        raise NotImplementedError


class SqliteTrackRepo(TrackRepo):
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA ENCODING='UTF-8'")
        self.load_min_max()

    def load_min_max(self):
        # TODO what happens when the DB is empty?
        q = "SELECT MIN(tempo), MAX(tempo), MIN(energy), MAX(energy), MIN(danceability), MAX(danceability) FROM tracks"
        res = self.cursor.execute(q).fetchone()
        self.min_max = { "tempo": (res[0], res[1]), "energy": (res[2], res[3]), "danceability": (res[4], res[5]) }

    # feature_constraints is array of tuples eg. ("energy", "<", 3.4)
    def get_random_tracks(self, count, feature_constraints):
        q = "SELECT track_id, track_name, file_path, tempo, energy, danceability, artist_name FROM tracks JOIN artists USING(artist_id) ORDER BY RANDOM() LIMIT ?"
        tracks = []
        for (track_id, track_name, file_path, tempo, energy, danceability, artist_name) in self.cursor.execute(q, (str(count),)):
            features = {
                "energy": energy,
                "tempo": tempo,
                "danceability": danceability,
                "rel_energy": self.rel_feature("energy", energy),
                "rel_tempo": self.rel_feature("tempo", tempo),
                "rel_danceability": self.rel_feature("danceability", danceability)
            }
            tracks.append(Track(unicode(track_name), unicode(artist_name), track_id, unicode(file_path), features))

        return tracks

    def rel_feature(self, feature_name, abs_value):
        mmin, mmax = self.min_max[feature_name]
        return (abs_value-mmin) / (mmax-mmin)

    @staticmethod
    def init_tables(db_file):
        cursor = sqlite3.connect(db_file).cursor()

        cursor.execute(""" CREATE TABLE artists (
            artist_id INTEGER PRIMARY KEY NOT NULL,
            artist_name TEXT NOT NULL UNIQUE
        )""")

        cursor.execute(""" CREATE TABLE tracks (
            track_id INTEGER PRIMARY KEY NOT NULL,
            artist_id INTEGER NOT NULL REFERENCES artists(artist_id),
            track_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            tempo REAL NOT NULL,
            energy REAL NOT NULL,
            danceability REAL NOT NULL
        )""")
        # putting the feature values directly to the track information makes searching simple and efficient
        # at least till we have a reasonable number of features