#!/usr/bin/python2
import kivy
kivy.require('1.9.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


class RootLayout(FloatLayout):
    pass

class TrackInfo(BoxLayout):
    pass

class Playlist(FloatLayout):

    track_info_width = NumericProperty(150)
    track_info_height = NumericProperty(50)
    track_info_count_x = NumericProperty(0)
    track_info_count_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)
    
    def update_counts(self):
        self.clear_widgets()
        self.track_info_count_x = self.width / self.track_info_width
        self.track_info_count_y = self.height / self.track_info_height
    
    def add_track_info(self, name1, name2, x, y):
        tr = TrackInfo()
        tr.width = self.track_info_width
        tr.height = self.track_info_height
        tr.x = self.x + x * self.track_info_width
        tr.y = self.y + y * self.track_info_height
        print(self.x, self.y)
        self.add_widget(tr)
    
    def on_size(self, *args):
        self.update_counts()
        self.clear_widgets()
        print("!!!", self.ids)
        if self.track_info_count_x == 0 or self.track_info_count_y == 0:
            print("!! cannot add now")
        else:
            self.add_track_info("x", "y", 0, 0)

   
class PlaylistApp(App):

    def build(self):
        return RootLayout()
    
    def on_start(self):
        Controller(self)

class Controller:

    def __init__(self, app):
        self.ids = app.root.ids
        self.playlist = self.ids.playlist
    

if __name__ == '__main__':
    PlaylistApp().run()