import os
import gi
from natsort import natsorted
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

class CustomWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to KrenkaOS")
        self.set_default_size(700, 500)
        self.set_resizable(True)
        self.set_decorated(False)

        # Default language is Czech

        self.language = "CZ"
        self.image_paths = []
        self.load_image_paths()

        self.current_image_index = 0

        # Create a fixed layout container

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        # Load CSS

        self.load_css()

        # Image container

        self.image_event_box = Gtk.EventBox()
        self.image_event_box.set_visible_window(True)
        self.image_event_box.set_name("image_box")
        self.fixed.put(self.image_event_box, 0, 0)

        self.image = Gtk.Image()
        self.image_event_box.add(self.image)

        # Labels

        self.label_krenka = Gtk.Label(label="KrenkaOS LTS")
        self.label_krenka.set_name("krenka_label")
        self.fixed.put(self.label_krenka, 265, 10)

        self.label_lang = Gtk.Label(label="Choose Language of the Guide:")
        self.label_lang.set_name("lang_label")
        self.fixed.put(self.label_lang, 220, 383)

        self.label_unof = Gtk.Label(label="Welcome to KrenkaOS 1e.25 LTS!")
        self.label_unof.set_name("unof_label")
        self.fixed.put(self.label_unof, 152, 345)

        # Navigation buttons

        self.button_next = Gtk.Button(label="Next")
        self.button_next.set_size_request(100, 40)
        self.button_next.connect("clicked", self.next_click)
        self.fixed.put(self.button_next, 590, 10)

        self.button_prev = Gtk.Button(label="Previous")
        self.button_prev.set_size_request(100, 40)
        self.button_prev.set_name("previous_button")
        self.button_prev.connect("clicked", self.prev_click)
        self.button_prev.hide()  # Initially hide the "Previous" button
        self.fixed.put(self.button_prev, 10, 10)

        # Language Selection Radio Buttons

        self.radio_button_cz = Gtk.RadioButton.new_with_label(None, "Čeština")
        self.radio_button_cz.set_name("radio_button")
        self.radio_button_cz.connect("toggled", self.lang_toggle, "CZ")
        self.fixed.put(self.radio_button_cz, 300, 420)

        self.radio_button_en = Gtk.RadioButton.new_with_label_from_widget(self.radio_button_cz, "English")
        self.radio_button_en.set_name("radio_button")
        self.radio_button_en.connect("toggled", self.lang_toggle, "EN")
        self.fixed.put(self.radio_button_en, 300, 448)

        # Set Czech as the default

        self.radio_button_cz.set_active(True)

        # Load and display the first image

        self.load_image()

        # Update buttons visibility after image load

        self.update_buttons()

        # Connect the "map" signal to update buttons after show_all() is processed.

        self.connect("map", self.on_map)

    def on_map(self, widget):

        # Called after the window is mapped (shown).
        self.update_buttons()

    def load_css(self):
        """Load CSS for the application."""
        css_provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles.css')
        if os.path.exists(css_path):
            try:
                css_provider.load_from_path(css_path)
            except Exception as e:
                print(f"Error loading CSS: {e}")
        else:
            print(f"Warning: CSS file '{css_path}' not found!")
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def load_image_paths(self):
        """Load image paths based on the selected language and ensure 'tux.png' is always first."""

        base_path = os.path.dirname(os.path.abspath(__file__))
        img_folder = "slides/cz/" if self.language == "CZ" else "slides/en/"
        full_path = os.path.join(base_path, img_folder)
        if os.path.exists(full_path):
            all_images = [os.path.join(full_path, f) for f in os.listdir(full_path)
                          if f.endswith((".png", ".jpg", ".jpeg"))]
            # Separate tux.png from other images
            tux_image = [img for img in all_images if "tux.png" in img]
            other_images = natsorted([img for img in all_images if "tux.png" not in img])
            # Combine tux first, then the rest
            self.image_paths = tux_image + other_images
        print(f"Language: {self.language}, Image Paths: {self.image_paths}")
        # Reset index only AFTER paths are updated
        self.current_image_index = 0

    def load_image(self):
        """Load and center the image while resizing to fit the window, and update visibility of labels & buttons."""

        img_path = self.image_paths[self.current_image_index]
        try:
            window_width, window_height = self.get_size()
            print(f"Window size: {window_width}x{window_height}")
            image_width = image_height = 0
            # Check if the current image is tux.png
            is_tux = "tux.png" in img_path
            if is_tux:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 217, 200, True)
                self.image.set_from_pixbuf(pixbuf)
                image_width, image_height = 217, 200
                self.image_event_box.get_style_context().remove_class("slide-background")
            else:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
                aspect_ratio = pixbuf.get_width() / pixbuf.get_height()
                if window_width / window_height > aspect_ratio:
                    image_width = int(window_height * aspect_ratio)
                    image_height = window_height
                else:
                    image_width = window_width
                    image_height = int(window_width / aspect_ratio)
                scaled_pixbuf = pixbuf.scale_simple(image_width, image_height, GdkPixbuf.InterpType.BILINEAR)
                self.image.set_from_pixbuf(scaled_pixbuf)
                self.image_event_box.get_style_context().add_class("slide-background")

            # Center the image_event_box (and thus the image)

            image_x = (window_width - image_width) // 2
            image_y = (window_height - image_height) // 2
            self.fixed.move(self.image_event_box, image_x, image_y)

            # Show radio buttons & labels only when Tux is visible

            self.label_lang.set_visible(is_tux)
            self.label_unof.set_visible(is_tux)
            self.radio_button_cz.set_visible(is_tux)
            self.radio_button_en.set_visible(is_tux)
            
        except Exception as e:
            print(f"Error loading image: {e}")
        # Ensure buttons are updated after image load
        self.update_buttons()

    def update_buttons(self):
        """Update visibility of Next/Previous buttons."""
        # Hide the "Previous" button if at the first image
        if self.current_image_index == 0:
            self.button_prev.hide()
        else:
            self.button_prev.show()
        # Hide the "Next" button if at the last image
        if self.current_image_index == len(self.image_paths) - 1:
            self.button_next.hide()
        else:
            self.button_next.show()

    def next_click(self, widget):
        """Go to the next image."""
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_image()

    def prev_click(self, widget):
        """Go to the previous image."""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    def lang_toggle(self, widget, lang):
        """Switch language and reload images."""
        if widget.get_active() and self.language != lang:
            self.language = lang
            self.load_image_paths()
            self.load_image()
        self.update_buttons()

win = CustomWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
