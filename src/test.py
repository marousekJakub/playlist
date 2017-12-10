from track import SqliteTrackRepo
r = SqliteTrackRepo("db2.sqlite")
print(r.get_random_tracks(4, []))
