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
        root = RootLayout(bg_path='/home/kuba/playlist2/src/party.jpg', features=self.features)
        root.choose_x.bind(text=self.update_axes)
        root.choose_y.bind(text=self.update_axes)
        return root

    def on_start(self):
        self.update_axes()

    def update_axes(self, *args):
        feature_x = self.root.choose_x.active_feature
        feature_y = self.root.choose_y.active_feature
        self.root.playlist.feature_x = feature_x
        self.root.playlist.feature_y = feature_y

        
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