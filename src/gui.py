# -*- coding: utf-8 -*-
import kivy
kivy.require('1.0.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from math import floor, ceil

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
    feature_x = ObjectProperty()
    feature_y = ObjectProperty()
    _cols = NumericProperty()
    _rows = NumericProperty()
    _cell_width = NumericProperty()
    _cell_height = NumericProperty()

    def __init__(self, **kwargs):
        super(Playlist, self).__init__(**kwargs)
        self.bind(size=self.size_update)
        self.widget_positions = {}
    
    def size_update(self, *size):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=(1,1,1,1))
            Line(points=[self.x, self.center_y, self.x + self.width, self.center_y])
            Line(points=[self.center_x, self.y, self.center_x, self.y + self.height])

        self._unregister_widgets()
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
        self._register_widget(col, row, widget)
        widget.center_x = self.x + (col+0.5) * self._cell_width
        widget.center_y = self.y + (row+0.5) * self._cell_height
        self.add_widget(widget)

    def _register_widget(self, col, row, widget):
        if not ( (0 <= col < self._cols) and (0 <= row <= self._rows) ):
            raise Exception("Attempt to place widget at non-existent position %d, %d" % (col, row))
        elif (col, row) in self.widget_positions:
            raise Exception("Attempt to place widget to occupied position %d %d" % (col, row))
        else:
            self.widget_positions[(col, row)] = widget
    
    def _unregister_widgets(self):
        self.clear_widgets()
        self.widget_positions.clear()
    
    def place_widget_central(self, widget):
        # central place in the playlist occupies a single column (if num_cols is odd)
        # or two columns in the middle (if num_cols is even)
        # the same for rows
        cols1 = (self._cols - 1) / 2.0
        rows1 = (self._rows - 1) / 2.0
        med_cols = range(int(cols1), int(ceil(cols1)) + 1)
        med_rows = range(int(rows1), int(ceil(rows1)) + 1)
        for col in med_cols:
            for row in med_rows:
                self._register_widget(col, row, widget)
        
        widget.center = self.center
        self.add_widget(widget)
    
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


class FeatureChoose(Spinner):
    def __init__(self, features, **kwargs):
        super(FeatureChoose, self).__init__(**kwargs)
        self.text = features[0].name_readable
        self.values = [ f.name_readable for f in features ]
        self.value_objects = features
        self.size_hint_x = None
        self.width = 200


class FeatureChooseLabel(Label):
    def __init__(self, **kwargs):
        super(FeatureChooseLabel, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = self.texture_size[0] + 40


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
    def __init__(self, features, **kwargs):
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
        self.bottom_bar = MenuBar()
        self.search = TextInput(multiline=False)
        self.choose_x = FeatureChoose(features)
        self.choose_y = FeatureChoose(features)
        self.choose_label_x = FeatureChooseLabel(text="X:")
        self.choose_label_y = FeatureChooseLabel(text="Y:")

        self.search.height = self.search.font_size + 15

        self.menu_bar.add_widget(self.add_track)
        self.menu_bar.add_widget(self.show_tracks)
        self.bottom_bar.add_widget(self.choose_label_x)
        self.bottom_bar.add_widget(self.choose_x)
        self.bottom_bar.add_widget(self.choose_label_y)
        self.bottom_bar.add_widget(self.choose_y)
        self.bottom_bar.add_widget(self.search)
        self.add_widget(self.menu_bar)
        self.add_widget(self.progress_bar)
        self.add_widget(self.playlist)
        self.add_widget(self.bottom_bar)

    
    def set_background(self, *args):
        if self.bg_path is not None:
            with self.canvas.before:
                Rectangle(source=self.bg_path, pos=(self.center_x - 2*500, self.center_y - 2*300), size=(2*1200, 2*600))