# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from math import floor

class TrackInfoLabel(Label):
    def __init__(self, track_info, **kwargs):
        super(TrackInfoLabel, self).__init__(**kwargs)
        self.halign = "left"
        self.width = track_info.width - 10
        self.height = self.font_size
        self.text_size = (track_info.width - 20, None)
        self.shorten = True


class TrackInfo(BoxLayout):
    track_artist = StringProperty()
    track_name = StringProperty()
    
    def __init__(self, **kwargs):
        super(TrackInfo, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.width = 150
        self.height = 50
        self.size_hint = (None, None)
        self.bind(pos=self.set_background)
        
        self.add_widget(TrackInfoLabel(self, text=self.track_artist))
        self.add_widget(TrackInfoLabel(self, text=self.track_name))
    
    def set_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(0.5, 0.5, 0.5, 1))
            Rectangle(pos=self.pos, size=self.size)


class Playlist(FloatLayout):
    elem_width = NumericProperty()
    elem_height = NumericProperty()
    _cols = NumericProperty()
    _rows = NumericProperty()
    _cell_width = NumericProperty()
    _cell_height = NumericProperty()

    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)
        self.bind(size=self.size_update)
        self.widget_positions = {}
    
    def size_update(self, *size):
        print("updating size")
        self.clear_widgets()
        self.widget_positions.clear()
        if self.elem_width == 0 or self.elem_height == 0:
            self._cols = self._rows = 0
            self._cell_width = self._cell_height = 0
        else:
            self._cols = int(floor(self.width / self.elem_width))
            self._rows = int(floor(self.height / self.elem_height))
            if self._cols > 0 and self._rows > 0:
                self._cell_width = int(floor(self.width / self._cols))
                self._cell_height = int(floor(self.height / self._rows))
            else:
                self._cell_width = self._cell_height = 0

    def place_widget(self, col, row, widget):
        if not ( (0 <= col < self._cols) and (0 <= row <= self._rows) ):
            raise Exception("Attempt to place widget at non-existent position %d, %d" % (col, row))
        elif (col, row) in self.widget_positions:
            raise Exception("Attemp to place widget to occupied position %d %d" % (col, row))
        else:
            widget.center_x = self.x + (col+0.5) * self._cell_width
            widget.center_y = self.y + (row+0.5) * self._cell_height
            self.add_widget(widget)
            self.widget_positions[(col, row)] = widget
    
    def is_widget_placed(self, col, row):
        return (col, row) in self.widget_positions

    def num_cols(self):
        return self._cols

    def num_rows(self):
        return self._rows


class MenuButton(Button):
    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = 200


class MenuBar(StackLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        self.orientation = 'tb-lr'
        self.size_hint_y = None
        self.height = 40
        self.bind(size=self.set_background, pos=self.set_background)
    
    def set_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(0, 0, 0.5, 0.6))
            Rectangle(pos=self.pos, size=self.size)


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.bg_path = None
        if "bg_path" in kwargs:
            self.bg_path = kwargs["bg_path"]
            del(kwargs["bg_path"])
        
        super(RootLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.bind(size=self.set_background)
        
        self.add_track = MenuButton(text=u"Přidat novou skladbu")
        self.show_tracks = MenuButton(text=u"Správce skladeb")
        self.menu_bar = MenuBar()
        self.progress_bar = ProgressBar(max=100, value=50, size_hint_y=None, height=5)
        self.playlist = Playlist(elem_width=160, elem_height=60)
        self.search = TextInput(multiline=False, size_hint_y=None)

        self.search.height = self.search.font_size + 15

        self.menu_bar.add_widget(self.add_track)
        self.menu_bar.add_widget(self.show_tracks)
        self.add_widget(self.menu_bar)
        self.add_widget(self.progress_bar)
        self.add_widget(self.playlist)
        self.add_widget(self.search)
    
    def set_background(self, *args):
        if self.bg_path is not None:
            with self.canvas.before:
                Rectangle(source=self.bg_path, pos=(self.center_x - 2*500, self.center_y - 2*300), size=(2*1200, 2*600))