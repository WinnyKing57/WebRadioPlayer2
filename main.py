import kivy
kivy.require('2.1.0') # Or your target Kivy version

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.properties import (
    ObjectProperty, StringProperty, BooleanProperty, ListProperty, NumericProperty
)
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex
from kivy import platform # To check platform if using pyjnius later (not used in this version)

# Attempt to import plyer.
try:
    from plyer import theme as plyer_theme
    PLYER_AVAILABLE = True
    print("Plyer library found. System theme detection might be available.")
except ImportError:
    PLYER_AVAILABLE = False
    plyer_theme = None # Placeholder
    print("Plyer library not found. System theme detection disabled.")
except Exception as e: # Catch other plyer import errors (e.g. missing OS components for plyer backends)
    PLYER_AVAILABLE = False
    plyer_theme = None
    print(f"Error importing Plyer or its theme facade: {e}. System theme detection disabled.")

import radio_logic # Assuming radio_logic.py is in the same directory
import data_manager  # Assuming data_manager.py is in the same directory

# --- Theme Constants ---
THEME_LIGHT = 'light'
THEME_DARK = 'dark'

class RadioApp(App):
    current_theme = StringProperty(THEME_DARK)
    theme_toggle_button_text = StringProperty("Switch to Light Mode") # New property

    # Color properties (app_bg_color, etc.) as defined before...
    app_bg_color = ListProperty(get_color_from_hex("#1C1C1E"))
    primary_text_color = ListProperty(get_color_from_hex("#E0E0E0"))
    secondary_text_color = ListProperty(get_color_from_hex("#8E8E93"))
    accent_color = ListProperty(get_color_from_hex("#0A84FF"))
    secondary_bg_color = ListProperty(get_color_from_hex("#2C2C2E"))
    input_bg_color = ListProperty(get_color_from_hex("#3A3A3C"))
    button_normal_bg_color = ListProperty(get_color_from_hex("#555555"))
    button_down_bg_color = ListProperty(get_color_from_hex("#007AFF"))
    button_play_bg_color = ListProperty(get_color_from_hex("#34C759"))
    button_stop_bg_color = ListProperty(get_color_from_hex("#FF453A"))
    scrollbar_color = ListProperty(get_color_from_hex("#0A84FF"))
    slider_thumb_color = ListProperty(get_color_from_hex("#0A84FF"))
    slider_track_color = ListProperty(get_color_from_hex("#0A84FF"))

    # Palettes (light_theme_palette, dark_theme_palette) as defined before...
    light_theme_palette = {
        "app_bg_color": get_color_from_hex("#F0F0F0"), "primary_text_color": get_color_from_hex("#333333"),
        "secondary_text_color": get_color_from_hex("#555555"), "accent_color": get_color_from_hex("#007AFF"),
        "secondary_bg_color": get_color_from_hex("#FFFFFF"), "input_bg_color": get_color_from_hex("#E0E0E0"),
        "button_normal_bg_color": get_color_from_hex("#DCDCDC"), "button_down_bg_color": get_color_from_hex("#0062CC"),
        "button_play_bg_color": get_color_from_hex("#4CD964"), "button_stop_bg_color": get_color_from_hex("#FF3B30"),
        "scrollbar_color": get_color_from_hex("#007AFF"), "slider_thumb_color": get_color_from_hex("#007AFF"),
        "slider_track_color": get_color_from_hex("#007AFF"),
    }
    dark_theme_palette = {
        "app_bg_color": get_color_from_hex("#1C1C1E"), "primary_text_color": get_color_from_hex("#E0E0E0"),
        "secondary_text_color": get_color_from_hex("#8E8E93"), "accent_color": get_color_from_hex("#0A84FF"),
        "secondary_bg_color": get_color_from_hex("#2C2C2E"), "input_bg_color": get_color_from_hex("#3A3A3C"),
        "button_normal_bg_color": get_color_from_hex("#555555"), "button_down_bg_color": get_color_from_hex("#007AFF"),
        "button_play_bg_color": get_color_from_hex("#34C759"), "button_stop_bg_color": get_color_from_hex("#FF453A"),
        "scrollbar_color": get_color_from_hex("#0A84FF"), "slider_thumb_color": get_color_from_hex("#0A84FF"),
        "slider_track_color": get_color_from_hex("#0A84FF"),
    }


    def apply_theme(self, theme_name):
        print(f"Applying theme: {theme_name}")
        palette = self.dark_theme_palette
        if theme_name == THEME_LIGHT:
            palette = self.light_theme_palette
            self.theme_toggle_button_text = "Switch to Dark Mode" # Update button text
        elif theme_name == THEME_DARK:
            palette = self.dark_theme_palette
            self.theme_toggle_button_text = "Switch to Light Mode" # Update button text
        else:
            print(f"Warning: Unknown theme '{theme_name}'. Defaulting to dark.")
            theme_name = THEME_DARK
            palette = self.dark_theme_palette
            self.theme_toggle_button_text = "Switch to Light Mode"

        for color_name, color_value in palette.items():
            if hasattr(self, color_name):
                setattr(self, color_name, color_value)

        self.current_theme = theme_name

    def toggle_theme(self):
        new_theme = THEME_LIGHT if self.current_theme == THEME_DARK else THEME_DARK
        self.apply_theme(new_theme) # apply_theme now also updates button text
        data_manager.save_setting('theme', self.current_theme)
        print(f"Theme preference '{self.current_theme}' saved.")

    def load_theme_preference(self):
        user_saved_theme = data_manager.load_setting('theme', None)
        if user_saved_theme and user_saved_theme in [THEME_LIGHT, THEME_DARK]:
            print(f"Using user-saved theme preference: {user_saved_theme}")
            return user_saved_theme
        elif user_saved_theme:
             print(f"Warning: Invalid saved theme '{user_saved_theme}'. Correcting and attempting system/default.")
             data_manager.save_setting('theme', None)

        if PLYER_AVAILABLE and plyer_theme:
            try:
                system_theme_value = plyer_theme.get_theme()
                print(f"Plyer system theme detection returned: '{system_theme_value}'")
                if isinstance(system_theme_value, str):
                    if 'dark' in system_theme_value.lower():
                        print("Detected system dark theme via Plyer.")
                        return THEME_DARK
                    elif 'light' in system_theme_value.lower():
                        print("Detected system light theme via Plyer.")
                        return THEME_LIGHT
                    else: print(f"Plyer returned unknown theme value: '{system_theme_value}'. Using app default.")
                else: print("Plyer theme value is not a string. Using app default.")
            except NotImplementedError: print("Plyer theme detection not implemented for this platform. Using app default.")
            except Exception as e: print(f"Error during Plyer theme detection: {e}. Using app default.")

        print(f"Using hardcoded default theme: {THEME_DARK}")
        return THEME_DARK

    def build(self):
        initial_theme = self.load_theme_preference()
        self.apply_theme(initial_theme) # This will also set the initial button text
        return MainLayout()

# --- Station List Item Widget ---
class StationListItem(BoxLayout):
    station_name = StringProperty(''); station_url = StringProperty('')
    is_currently_favorite = BooleanProperty(False); app_root = ObjectProperty(None)
    def __init__(self, station_data, app_root_ref, **kwargs):
        super().__init__(**kwargs)
        self.station_name = station_data.get('name', 'Unknown Radio'); self.station_url = station_data.get('url', '')
        self.app_root = app_root_ref; self.update_favorite_status()
    def update_favorite_status(self): self.is_currently_favorite = radio_logic.is_favorite(self.station_url)
    def on_favorite_button_press(self, button_instance):
        if not self.station_url: return
        station_data = {'name': self.station_name, 'url': self.station_url}
        if self.is_currently_favorite: radio_logic.remove_from_favorites(self.station_url)
        else: radio_logic.add_to_favorites(station_data)
        self.update_favorite_status()
    def on_play_button_press(self):
        if self.station_url and self.app_root: self.app_root.play_station(self.station_url, self.station_name)

# --- Main Layout Widget ---
class MainLayout(BoxLayout):
    radio_list_layout = ObjectProperty(None); custom_station_name_input = ObjectProperty(None)
    custom_station_url_input = ObjectProperty(None); add_custom_status_label = ObjectProperty(None)
    currently_playing_label = ObjectProperty(None); volume_slider = ObjectProperty(None)
    current_sound = None; last_played_station_name = StringProperty("Stopped")
    _notification_popup = None; _error_popup = None
    def __init__(self, **kwargs): super().__init__(**kwargs); Clock.schedule_once(self.load_and_display_stations, 0)
    def show_error_popup(self, title, message):
        if self._error_popup: self._error_popup.dismiss()
        content = Label(text=message, font_size='16sp', halign='center', valign='middle', text_size=(self.width*0.7 if self.width else 500, None)) # Added width check
        self._error_popup = Popup(title=title, content=content, size_hint=(0.8, 0.4), auto_dismiss=True)
        self._error_popup.open()
    def load_and_display_stations(self, dt=None):
        if not self.radio_list_layout: self.show_error_popup("UI Error", "Radio list not ready."); return
        self.radio_list_layout.clear_widgets()
        self.radio_list_layout.add_widget(Label(text="Loading stations...", font_size='18sp', size_hint_y=None, height='50dp'))
        data_manager.ensure_data_dir_exists(); Clock.schedule_once(self._perform_station_loading, 0.1)
    def _perform_station_loading(self, dt=None):
        all_stations, new_fetched_stations = radio_logic.get_all_display_stations()
        self.radio_list_layout.clear_widgets()
        if all_stations:
            for station_data in all_stations: self.radio_list_layout.add_widget(StationListItem(station_data=station_data, app_root_ref=self))
        else: self.radio_list_layout.add_widget(Label(text="Could not load stations. Check internet or add custom radios.", halign='center', padding_x=20))
        if new_fetched_stations: self.show_notification("Nouvelle radio ajoutée !")
    def show_notification(self, message_text, duration=5):
        if self._notification_popup: self._notification_popup.dismiss()
        content = Label(text=message_text, font_size='16sp', halign='center', valign='middle'); content.bind(size=content.setter('text_size'))
        popup = Popup(title='Notification', content=content, size_hint=(None, None), size=('350dp', '120dp'), auto_dismiss=False)
        self._notification_popup = popup; popup.open(); Clock.schedule_once(lambda dt_ignore: self.dismiss_notification_popup(popup), duration)
    def dismiss_notification_popup(self, popup_instance):
        if popup_instance:
            try: popup_instance.dismiss()
            except Exception as e: print(f"Error dismissing notification: {e}")
            if self._notification_popup == popup_instance: self._notification_popup = None
    def add_custom_station_ui(self):
        if not all([self.custom_station_name_input, self.custom_station_url_input, self.add_custom_status_label]): self.show_error_popup("UI Error", "Input fields not ready."); return
        name = self.custom_station_name_input.text.strip(); url = self.custom_station_url_input.text.strip()
        if not name or not url: self.add_custom_status_label.text = "Name and URL required."; return
        if not (url.startswith('http://') or url.startswith('https://')): self.add_custom_status_label.text = "URL must start with http(s)://"; return
        if radio_logic.add_custom_station(name, url):
            self.add_custom_status_label.text = f"Added: {name}"; self.custom_station_name_input.text = ""; self.custom_station_url_input.text = ""
            self._perform_station_loading()
        else: self.add_custom_status_label.text = f"Already exists or invalid: {name}"
    def play_station(self, station_url, station_name):
        self.stop_audio(); self.last_played_station_name = f"Loading: {station_name}..."
        self.current_sound = SoundLoader.load(station_url)
        if self.current_sound:
            self.current_sound.bind(on_play=self.on_sound_play, on_stop=self.on_sound_stop)
            if self.volume_slider: self.current_sound.volume = self.volume_slider.value
            self.current_sound.play()
        else:
            error_message = f"Error: Could not load {station_name}."; self.last_played_station_name = f"Failed: {station_name}"
            self.show_error_popup("Playback Error", error_message)
    def stop_audio(self):
        if self.current_sound: self.current_sound.stop(); self.current_sound.unload(); self.current_sound = None
        self.last_played_station_name = "Stopped"
    def on_sound_play(self, instance): current_name_playing = self.last_played_station_name.replace("Loading: ", "").replace("...", ""); self.last_played_station_name = f"Playing: {current_name_playing}"
    def on_sound_stop(self, instance):
        if self.current_sound: original_name = self.last_played_station_name.replace("Playing: ", "").replace("Loading: ", "").replace("...", ""); self.last_played_station_name = f"Stream Ended: {original_name}"; self.current_sound.unload(); self.current_sound = None
    def on_volume_change(self, instance, value):
        if self.current_sound: self.current_sound.volume = value

# --- Main Execution ---
if __name__ == '__main__':
    data_manager.ensure_data_dir_exists()
    RadioApp().run()
