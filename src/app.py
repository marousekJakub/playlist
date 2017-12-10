#!/usr/bin/python2
# -*- coding: utf-8 -*-

from kivy.app import App
from gui import TrackInfo, RootLayout

class PlaylistApp(App):
    def build(self):
        return RootLayout(bg_path='/home/kuba/playlist2/src/party.jpg')       

if __name__ == '__main__':
    PlaylistApp().run()