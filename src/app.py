#!/usr/bin/python2
# -*- coding: utf-8 -*-

from kivy.app import App
from gui import TrackInfo, RootLayout
from track import Track, SqliteTrackRepo
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class PlaylistApp(App):
    def __init__(self, track_repo, features):
        super(PlaylistApp, self).__init__()
        self.repo = track_repo
        self.features = features
        self.current_track_info = None
        self.current_sound = None
        self.current_sound_pos = None

    def build(self):
        root = RootLayout(bg_path='/home/kuba/playlist2/src/party.jpg', features=self.features)
        root.choose_x.bind(text=self.update_axes)
        root.choose_x.bind(text=self.update_tracks)
        root.choose_y.bind(text=self.update_axes)
        root.choose_y.bind(text=self.update_tracks)
        root.playlist.bind(size=self.update_tracks)
        return root

    def on_start(self):
        self.update_axes()
        self.update_tracks()
        Clock.schedule_interval(self.update_countdown, 1/10.0)

    def update_axes(self, *args):
        feature_x = self.root.choose_x.active_feature
        feature_y = self.root.choose_y.active_feature
        self.root.playlist.feature_x = feature_x
        self.root.playlist.feature_y = feature_y
    
    def update_tracks(self, *args):
        # cleanup the playlist
        playlist = self.root.playlist
        if playlist.num_cols() == 0 or playlist.num_rows() == 0:
            return
        playlist.cells_reset()

        # select the central feature values, place the central TrackInfo when necessary
        feature_x = self.root.playlist.feature_x
        feature_y = self.root.playlist.feature_y
        if self.current_track_info is None:
            center_x = center_y = 0.5
        else:
            center_x = self.current_track_info.track.features[feature_x.name]
            center_y = self.current_track_info.track.features[feature_y.name]
            playlist.place_widget_central(self.current_track_info)
        
        # get the tracks
        num_tracks = (playlist.num_cols() * playlist.num_rows()) / 6
        for track in self.repo.get_random_tracks(num_tracks, []):

            feat_val_x = track.features[feature_x.name]
            feat_val_y = track.features[feature_y.name]
            if 0 <= feat_val_x < center_x:
                good_x = feat_val_x/(2.0*center_x) if center_x != 0 else 0
            elif center_x <= feat_val_x <= 1:
                good_x = (feat_val_x-center_x)/(2.0-2*center_x) + 0.5 if center_x != 1 else 1
            else:
                assert False
            if 0 <= feat_val_y < center_y:
                good_y = feat_val_y/(2.0*center_y) if center_y != 0 else 0
            elif center_y <= feat_val_y <= 1:
                good_y = (feat_val_y-center_y)/(2.0-2*center_y) + 0.5 if center_y != 1 else 1
            else:
                assert False
            
            good_x = int(round(good_x * (playlist.num_cols()-1)))
            good_y = int(round(good_y * (playlist.num_rows()-1)))
            if not playlist.is_widget_placed(good_x, good_y):
                tr = TrackInfo(track=track)
                tr.bind(on_touch_up=self.track_chosen)
                playlist.place_widget(good_x, good_y, tr)
            else:
                pass # TODO
        
        self.root.progress_bar.value = 100
    
    def update_countdown(self, *args):
        progress_bar = self.root.progress_bar
        if progress_bar.value <= 0:
            self.update_tracks()
        else:
            progress_bar.value -= 2
    
    def track_chosen(self, track_info, event):
        if track_info.collide_point(event.x, event.y):
            self.current_track_info = track_info
            if track_info.is_active:
                if self.current_sound.state == "play":
                    self.current_sound_pos = self.current_sound.get_pos()
                    self.current_sound.stop()
                else:
                    self.current_sound.play()
                    self.current_sound.seek(self.current_sound_pos)
                    self.current_sound_pos = None
            else:
                track_info.is_active = True
                
                if self.current_sound is not None:
                    self.current_sound.stop()
                    self.current_sound.unload()
                self.current_sound = SoundLoader.load(track_info.track.file_path)
                self.current_sound.play()
                self.update_tracks()

        
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