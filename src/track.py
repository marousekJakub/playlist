import sqlite3

class Track:
    def __init__(self, name, artist=None, Id=None, features=None):
        self.id = Id
        self.name = name
        self.artist = artist
        self.features = features
    
    def feature(self, feat_name, default=None):
        return self.features.get(feat_name, default)


class TrackRepo:
    def __init__(self):
        raise NotImplementedError("This class cannot be used separately")
    
    def get_random_songs(self, num, feature_constraints):
        raise NotImplementedError()


class SqliteTrackRepo(TrackRepo):
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
    
    def init_tables(self):
        self.cursor.execute(""" CREATE TABLE tracks (
            track_id INTEGER PRIMARY KEY NOT NULL,
            track_name VARCHAR(100) NOT NULL,
            artist_id VARCHAR(100) NOT NULL,
            file_path VARCHAR(100) NOT NULL
        )""")
           
        self.cursor.execute(""" CREATE TABLE artists (
            artist_id INTEGER PRIMARY KEY NOT NULL,
            artist_name VARCHAR(100) NOT NULL UNIQUE
        )""")

        self.cursor.execute(""" CREATE TABLE features (
            feature_id INTEGER PRIMARY KEY NOT NULL,
            feature_name VARCHAR(30) NOT NULL UNIQUE
        )""")
