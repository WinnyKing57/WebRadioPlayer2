import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton # Good for favorite state
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader # For audio playback
from kivy.uix.slider import Slider # For volume control
from kivy.uix.popup import Popup # For notifications

import radio_logic
import data_manager

# Define a custom widget for each station in the list
class StationListItem(BoxLayout):
    station_name = StringProperty('')
    station_url = StringProperty('')
    is_currently_favorite = BooleanProperty(False)
    # Add a reference to the main app's root widget to call its methods
    app_root = ObjectProperty(None)

    def __init__(self, station_data, app_root_ref, **kwargs):
        super().__init__(**kwargs)
        self.station_name = station_data.get('name', 'Unknown Radio')
        self.station_url = station_data.get('url', '')
        self.app_root = app_root_ref # Store reference to MainLayout
        self.update_favorite_status()

    def update_favorite_status(self):
        self.is_currently_favorite = radio_logic.is_favorite(self.station_url)

    def on_favorite_button_press(self, button_instance):
        if not self.station_url: return
        station_data = {'name': self.station_name, 'url': self.station_url}
        if self.is_currently_favorite:
            radio_logic.remove_from_favorites(self.station_url)
        else:
            radio_logic.add_to_favorites(station_data)
        self.update_favorite_status()

    def on_play_button_press(self):
        if self.station_url and self.app_root:
            print(f"UI: Play button pressed for {self.station_name}")
            self.app_root.play_station(self.station_url, self.station_name)
        else:
            print(f"UI Error: Missing URL or app_root reference in StationListItem for {self.station_name}")

class MainLayout(BoxLayout):
    radio_list_layout = ObjectProperty(None)
    custom_station_name_input = ObjectProperty(None)
    custom_station_url_input = ObjectProperty(None)
    add_custom_status_label = ObjectProperty(None)
    currently_playing_label = ObjectProperty(None)
    volume_slider = ObjectProperty(None)

    current_sound = None
    last_played_station_name = StringProperty("N/A")
    _notification_popup = None # To keep a reference

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.load_and_display_stations, 0)
        self.last_played_station_name = "Stopped"

    def load_and_display_stations(self, dt=None):
        print("UI: Loading and displaying ALL stations.")
        data_manager.ensure_data_dir_exists()
        all_stations, new_fetched_stations = radio_logic.get_all_display_stations()

        if self.radio_list_layout is None:
            print("UI Error: radio_list_layout is None.")
            return

        self.radio_list_layout.clear_widgets()
        if all_stations:
            for station_data in all_stations:
                item = StationListItem(station_data=station_data, app_root_ref=self)
                self.radio_list_layout.add_widget(item)
        else:
            self.radio_list_layout.add_widget(Label(text="Could not load any radio stations."))

        if new_fetched_stations: # Check if the list is not empty
            print(f"UI: {len(new_fetched_stations)} new fetched station(s) detected. Triggering notification.")
            self.show_notification("Nouvelle radio ajoutée !") # Single notification

    def show_notification(self, message_text, duration=5):
        if self._notification_popup and self._notification_popup.content:
            self._notification_popup.dismiss() # Dismiss previous one if any
            self._notification_popup = None

        content = Label(text=message_text, font_size='16sp', halign='center', valign='middle')
        content.bind(size=content.setter('text_size')) # For text wrapping

        popup = Popup(title='Notification',
                      content=content,
                      size_hint=(None, None), size=('350dp', '120dp'), # Adjusted size
                      auto_dismiss=False)
        self._notification_popup = popup
        popup.open()
        Clock.schedule_once(lambda dt: self.dismiss_notification_popup(popup), duration)
        print(f"Notification displayed: '{message_text}' for {duration}s")

    def dismiss_notification_popup(self, popup_instance):
        if popup_instance: # Check if it hasn't been dismissed by other means
            try:
                popup_instance.dismiss()
                if self._notification_popup == popup_instance:
                    self._notification_popup = None
                print("Notification dismissed by timer.")
            except Exception as e:
                print(f"Error dismissing popup: {e}") # Kivy can sometimes have issues if popup already removed


    def add_custom_station_ui(self):
        if not self.custom_station_name_input or not self.custom_station_url_input or not self.add_custom_status_label: return
        name = self.custom_station_name_input.text.strip()
        url = self.custom_station_url_input.text.strip()
        if not name or not url:
            self.add_custom_status_label.text = "Name and URL cannot be empty."; return
        if radio_logic.add_custom_station(name, url):
            self.add_custom_status_label.text = f"Added: {name}"
            self.custom_station_name_input.text = ""; self.custom_station_url_input.text = ""
            self.load_and_display_stations()
        else:
            self.add_custom_status_label.text = f"Already exists or invalid: {name}"

    def play_station(self, station_url, station_name):
        self.stop_audio()
        self.current_sound = SoundLoader.load(station_url)
        if self.current_sound:
            self.current_sound.bind(on_play=self.on_sound_play, on_stop=self.on_sound_stop)
            self.current_sound.volume = self.volume_slider.value if self.volume_slider else 1.0
            self.current_sound.play()
            self.last_played_station_name = f"Playing: {station_name}"
            if self.currently_playing_label: self.currently_playing_label.text = self.last_played_station_name
        else:
            self.last_played_station_name = f"Error loading: {station_name}"
            if self.currently_playing_label: self.currently_playing_label.text = self.last_played_station_name

    def stop_audio(self):
        if self.current_sound:
            self.current_sound.stop(); self.current_sound.unload(); self.current_sound = None
        self.last_played_station_name = "Stopped"
        if self.currently_playing_label: self.currently_playing_label.text = self.last_played_station_name

    def on_sound_play(self, instance): print(f"Sound started playing: {self.last_played_station_name}")
    def on_sound_stop(self, instance): print(f"Sound stopped: {self.last_played_station_name}")

    def on_volume_change(self, instance, value):
        if self.current_sound: self.current_sound.volume = value
        print(f"Volume changed to: {value:.2f}")

class RadioApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    data_manager.ensure_data_dir_exists()
    RadioApp().run()
