#!/usr/bin/python2
# -*- coding: utf-8 -*-

from kivy.app import App
from gui import TrackInfo, RootLayout
from track import Track, SqliteTrackRepo


class PlaylistApp(App):
    def __init__(self, track_repo, features):
        super(PlaylistApp, self).__init__()
        self.repo = track_repo
        self.features = features
        self.current_track = None

    def build(self):
        self.rl = RootLayout(bg_path='/home/kuba/playlist2/src/party.jpg', features=self.features)
        # self.rl.playlist.bind(size=self.update_playlist)
        return self.rl
        
class Feature:
    def __init__(self, name, name_readable, low_readable, high_readable):
        self.name = name
        self.name_readable = name_readable
        self.low_readable = low_readable
        self.high_readable = high_readable

standard_features = [
    Feature("rel_energy", "Energy", "Less energic", "More energic"),
    Feature("rel_tempo", "Tempo", "Slower", "Faster"),
    Feature("rel_danceability", "Danceability", "Less danceable", "More danceable"),
]

if __name__ == '__main__':
    PlaylistApp(SqliteTrackRepo("db2.sqlite"), standard_features).run()