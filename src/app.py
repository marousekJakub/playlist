#!/usr/bin/python2
# -*- coding: utf-8 -*-

from kivy.app import App
from gui import TrackInfo, RootLayout

class PlaylistApp(App):
    def build(self):
        rl = RootLayout(bg_path='/home/kuba/playlist2/src/party.jpg')
        rl.playlist.bind(size=self.place_test_widgets)
        return rl
    
    def place_test_widgets(self, *args):
        p = self.root.playlist
        print(p.num_rows(), p.num_cols())
        if p.num_rows() > 0 and p.num_cols() > 0:
            for col in range(p.num_cols()):
                for row in range(p.num_rows()):
                    p.place_widget(col, row, TrackInfo(track_artist="artist", track_name="name"))


if __name__ == '__main__':
    PlaylistApp().run()