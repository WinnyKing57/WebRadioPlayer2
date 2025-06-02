import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup

import radio_logic
import data_manager

# Define a custom widget for each station in the list
class StationListItem(BoxLayout):
    station_name = StringProperty('')
    station_url = StringProperty('')
    is_currently_favorite = BooleanProperty(False)
    app_root = ObjectProperty(None)

    def __init__(self, station_data, app_root_ref, **kwargs):
        super().__init__(**kwargs)
        self.station_name = station_data.get('name', 'Unknown Radio')
        self.station_url = station_data.get('url', '')
        self.app_root = app_root_ref
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
    last_played_station_name = StringProperty("Stopped") # Initialized
    _notification_popup = None
    _error_popup = None # For displaying more persistent errors

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.load_and_display_stations, 0)
        # self.last_played_station_name is already initialized by StringProperty

    def show_error_popup(self, title, message):
        """Displays a general error popup."""
        if self._error_popup:
            self._error_popup.dismiss()
            self._error_popup = None

        content = Label(text=message, font_size='16sp', halign='center', valign='middle')
        content.bind(size=content.setter('text_size'))

        self._error_popup = Popup(title=title,
                                 content=content,
                                 size_hint=(0.8, 0.4), # Larger popup for errors
                                 auto_dismiss=True) # User can click outside to dismiss
        self._error_popup.open()

    def load_and_display_stations(self, dt=None):
        print("UI: Loading and displaying ALL stations.")
        if self.radio_list_layout is None:
            print("UI Critical Error: radio_list_layout is None. Cannot proceed.")
            self.show_error_popup("UI Error", "Cannot display station list. Please restart.")
            return

        # Simple loading message
        self.radio_list_layout.clear_widgets()
        loading_label = Label(text="Loading stations...", font_size='18sp', size_hint_y=None, height='50dp')
        self.radio_list_layout.add_widget(loading_label)

        data_manager.ensure_data_dir_exists() # Ensure it exists before logic runs

        # Schedule the actual loading to allow the "Loading..." message to display
        Clock.schedule_once(self._perform_station_loading, 0.1)


    def _perform_station_loading(self, dt=None):
        all_stations, new_fetched_stations = radio_logic.get_all_display_stations()

        self.radio_list_layout.clear_widgets() # Clear "Loading..." or previous items

        if all_stations:
            for station_data in all_stations:
                item = StationListItem(station_data=station_data, app_root_ref=self)
                self.radio_list_layout.add_widget(item)
        else:
            # More informative error/empty state message
            error_msg = "Could not load radio stations.\nPlease check your internet connection or try again later.\nYou can still add custom radio stations below."
            # Create a label that can wrap text. text_size is important.
            # The width for text_size should ideally be bound to the width of its container.
            # For GridLayout with cols=1, it's roughly self.radio_list_layout.width.
            # Subtracting padding if any.
            error_label = Label(text=error_msg, halign='center', padding_x=20)
            error_label.bind(width=lambda *x: error_label.setter('text_size')(error_label, (error_label.width, None)))
            self.radio_list_layout.add_widget(error_label)
            # Optionally, show a popup for critical fetch failure
            # self.show_error_popup("Station Load Failed", "Failed to fetch the main radio list.")


        if new_fetched_stations:
            print(f"UI: {len(new_fetched_stations)} new fetched station(s) detected. Triggering notification.")
            self.show_notification("Nouvelle radio ajoutée !")

    def show_notification(self, message_text, duration=5):
        if self._notification_popup and self._notification_popup.content:
            self._notification_popup.dismiss()
            self._notification_popup = None
        content = Label(text=message_text, font_size='16sp', halign='center', valign='middle')
        content.bind(size=content.setter('text_size'))
        popup = Popup(title='Notification', content=content,
                      size_hint=(None, None), size=('350dp', '120dp'),
                      auto_dismiss=False)
        self._notification_popup = popup
        popup.open()
        Clock.schedule_once(lambda dt_ignore: self.dismiss_notification_popup(popup), duration)

    def dismiss_notification_popup(self, popup_instance):
        if popup_instance:
            try:
                popup_instance.dismiss()
                if self._notification_popup == popup_instance: self._notification_popup = None
            except Exception as e: print(f"Error dismissing notification popup: {e}")

    def add_custom_station_ui(self):
        if not all([self.custom_station_name_input, self.custom_station_url_input, self.add_custom_status_label]):
            self.show_error_popup("UI Error", "Input fields are not ready.")
            return
        name = self.custom_station_name_input.text.strip()
        url = self.custom_station_url_input.text.strip()

        if not name or not url:
            self.add_custom_status_label.text = "Name and URL cannot be empty."
            return
        # Basic URL validation hint
        if not (url.startswith('http://') or url.startswith('https://')):
            self.add_custom_status_label.text = "URL should start with http:// or https://"
            return

        if radio_logic.add_custom_station(name, url):
            self.add_custom_status_label.text = f"Added: {name}"
            self.custom_station_name_input.text = ""; self.custom_station_url_input.text = ""
            self._perform_station_loading() # Refresh list
        else:
            self.add_custom_status_label.text = f"Already exists or invalid: {name}"

    def play_station(self, station_url, station_name):
        print(f"Attempting to play: {station_name} ({station_url})")
        self.stop_audio()
        self.last_played_station_name = f"Loading: {station_name}..." # Update UI immediately

        self.current_sound = SoundLoader.load(station_url)
        if self.current_sound:
            self.current_sound.bind(on_play=self.on_sound_play, on_stop=self.on_sound_stop)
            self.current_sound.volume = self.volume_slider.value if self.volume_slider else 1.0
            self.current_sound.play()
            # on_sound_play will update the label to "Playing..."
        else:
            error_message = f"Error: Could not load {station_name}.\nCheck URL or stream format."
            print(error_message)
            self.last_played_station_name = f"Failed: {station_name}"
            self.show_error_popup("Playback Error", error_message)


    def stop_audio(self):
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound.unload()
            self.current_sound = None
        self.last_played_station_name = "Stopped"

    def on_sound_play(self, instance):
        current_name_playing = self.last_played_station_name.replace("Loading: ", "").replace("...", "")
        self.last_played_station_name = f"Playing: {current_name_playing}"
        print(f"Sound started playing for: {current_name_playing}")

    def on_sound_stop(self, instance):
        if self.current_sound is not None:
            print(f"Sound for {self.last_played_station_name} stopped unexpectedly (stream ended or error).")
            self.last_played_station_name = f"Stream Ended: {self.last_played_station_name.replace('Playing: ', '').replace('Loading: ', '')}"
            self.current_sound.unload()
            self.current_sound = None
        else:
            print(f"Sound stopped (likely user-initiated or after error handling).")


    def on_volume_change(self, instance, value):
        if self.current_sound:
            self.current_sound.volume = value
        # print(f"Volume changed to: {value:.2f}") # Reduce verbose logging

class RadioApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    data_manager.ensure_data_dir_exists()
    RadioApp().run()
