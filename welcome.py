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

        self.language = "CZ"
        self.image_paths = []
        self.current_image_index = 0

        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        self.load_css()
        self.load_image_paths()

        self.image_event_box = Gtk.EventBox()
        self.image_event_box.set_visible_window(True)
        self.image_event_box.set_name("image_box")
        self.fixed.put(self.image_event_box, 0, 0)

        self.image = Gtk.Image()
        self.image_event_box.add(self.image)

        self.label_krenka = Gtk.Label(label="KrenkaOS LTS")
        self.label_krenka.set_name("krenka_label")
        self.fixed.put(self.label_krenka, 265, 10)

        self.label_lang = Gtk.Label(label="Choose Language of the Guide:")
        self.label_lang.set_name("lang_label")
        self.fixed.put(self.label_lang, 220, 383)

        self.label_unof = Gtk.Label(label="Welcome to KrenkaOS 1e.25 LTS!")
        self.label_unof.set_name("unof_label")
        self.fixed.put(self.label_unof, 152, 345)

        self.button_next = Gtk.Button(label="Next")
        self.button_next.set_name("next_button")
        self.button_next.set_size_request(100, 40)
        self.button_next.connect("clicked", self.next_click)
        self.fixed.put(self.button_next, 590, 10)

        self.button_prev = Gtk.Button(label="Previous")
        self.button_prev.set_size_request(100, 40)
        self.button_prev.set_name("previous_button")
        self.button_prev.connect("clicked", self.prev_click)
        self.button_prev.hide()
        self.fixed.put(self.button_prev, 10, 10)

        self.button_exit = Gtk.Button(label="Exit")
        self.button_exit.set_size_request(100, 40)
        self.button_exit.set_name("exit_button")
        self.button_exit.connect("clicked", Gtk.main_quit)
        self.button_exit.hide()
        self.fixed.put(self.button_exit, 590, 450)

        self.radio_button_cz = Gtk.RadioButton.new_with_label(None, "Čeština")
        self.radio_button_cz.set_name("radio_button")
        self.radio_button_cz.connect("toggled", self.lang_toggle, "CZ")
        self.fixed.put(self.radio_button_cz, 300, 420)

        self.radio_button_en = Gtk.RadioButton.new_with_label_from_widget(self.radio_button_cz, "English")
        self.radio_button_en.set_name("radio_button")
        self.radio_button_en.connect("toggled", self.lang_toggle, "EN")
        self.fixed.put(self.radio_button_en, 300, 448)

        self.radio_button_cz.set_active(True)

        self.link_button_website = Gtk.LinkButton(uri="https://example.com", label="Web")
        self.fixed.put(self.link_button_website, 100, 270)

        self.link_button_discord = Gtk.LinkButton(uri="https://discord.com", label="Discord")
        self.fixed.put(self.link_button_discord, 300, 270)

        self.link_button_github = Gtk.LinkButton(uri="https://github.com", label="GitHub")
        self.fixed.put(self.link_button_github, 500, 270)

        self.load_image()
        self.update_buttons()
        self.connect("map", self.on_map)

    def on_map(self, widget):
        self.update_buttons()

    def load_css(self):
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
        """
        Load image paths and order them so that:
         - The welcome slide (e.g. tux.png) comes first,
         - then slide1.png,
         - then slide2.png,
         - then slide3.png,
         - then slide4.png,
         - and then any remaining images.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        img_folder = "slides/cz/" if self.language == "CZ" else "slides/en/"
        full_path = os.path.join(base_path, img_folder)

        if os.path.exists(full_path):
            all_images = [os.path.join(full_path, f) for f in os.listdir(full_path)
                          if f.endswith((".png", ".jpg", ".jpeg"))]

            # Specifically handle tux.png, slide1.png, slide2.png, slide3.png, and slide4.png
            tux_image = [img for img in all_images if "tux.png" in img]
            slide1_image = [img for img in all_images if "slide1.png" in img]
            slide2_image = [img for img in all_images if "slide2.png" in img]
            slide3_image = [img for img in all_images if "slide3.png" in img]
            slide4_image = [img for img in all_images if "slide4.png" in img]

            # Sort the other images
            other_images = natsorted([img for img in all_images
                                      if all(x not in img for x in ["tux.png", "slide1.png", "slide2.png", "slide3.png", "slide4.png"])])

            # Combine the image paths in the desired order
            self.image_paths = tux_image + slide1_image + slide2_image + slide3_image + slide4_image + other_images

        print(f"Language: {self.language}, Image Paths: {self.image_paths}")
        self.current_image_index = 0

    def load_image(self):
        """
        Load and resize the image to fit the window while maintaining its aspect ratio.
         - If the image is 'tux.png', use fixed dimensions.
         - For other images, fit within the window.
         - If the image is 'slide2.png', increase its size by 15% of the computed size.
         - The language selection controls are only shown when the image is 'tux.png'.
        """
        if not self.image_paths:
            print("No images found!")
            return

        img_path = self.image_paths[self.current_image_index]

        try:
            window_width, window_height = self.get_size()
            print(f"Window size: {window_width}x{window_height}")

            is_tux = "tux.png" in img_path
            is_slide2 = "slide2.png" in img_path
            is_slide3 = "slide3.png" in img_path
            is_slide4 = "slide4.png" in img_path

            if is_tux:
                # Tux: use fixed dimensions.
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 217, 200, True)
                image_width, image_height = 217, 200
                self.image_event_box.get_style_context().remove_class("slide-background")
            else:
                # For other slides, compute best fit within the window.
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(img_path)
                original_width = pixbuf.get_width()
                original_height = pixbuf.get_height()
                aspect_ratio = original_width / original_height

                if window_width / window_height > aspect_ratio:
                    image_width = int(window_height * aspect_ratio)
                    image_height = window_height
                else:
                    image_width = window_width
                    image_height = int(window_width / aspect_ratio)

                # If this is slide2, increase its dimensions by 15%.
                if is_slide2:
                    image_width = int(image_width * 0.85)
                    image_height = int(image_height * 0.85)

                if is_slide3:
                    image_width = int(image_width * 0.85)
                    image_height = int(image_height * 0.85)

                # If it's slide3 or slide4, no scaling adjustment is applied yet
                pixbuf = pixbuf.scale_simple(image_width, image_height, GdkPixbuf.InterpType.BILINEAR)
                self.image_event_box.get_style_context().add_class("slide-background")

            self.image.set_from_pixbuf(pixbuf)

            # Center the image.
            image_x = (window_width - image_width) // 2
            image_y = (window_height - image_height) // 2
            self.fixed.move(self.image_event_box, image_x, image_y)


            if is_slide4:
                self.fixed.move(self.image_event_box, image_x, 65)
                self.button_exit.show()

            # Show the language selection controls only when displaying tux.png.
            if is_tux:
                self.label_lang.set_visible(True)
                self.label_unof.set_visible(True)
                self.radio_button_cz.set_visible(True)
                self.radio_button_en.set_visible(True)
            else:
                self.label_lang.set_visible(False)
                self.label_unof.set_visible(False)
                self.radio_button_cz.set_visible(False)
                self.radio_button_en.set_visible(False)


        except Exception as e:
            print(f"Error loading image: {e}")

        self.update_buttons()

    def update_buttons(self):
        """Update the visibility of the navigation buttons."""
        self.button_prev.set_visible(self.current_image_index > 0)
        self.button_next.set_visible(self.current_image_index < len(self.image_paths) - 1)
        self.link_button_discord.set_visible(self.current_image_index == 4)
        self.link_button_github.set_visible(self.current_image_index == 4)
        self.link_button_website.set_visible(self.current_image_index == 4)
        self.button_exit.set_visible(self.current_image_index == 4)

    def next_click(self, widget):
        """Advance to the next image."""
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_image()

    def prev_click(self, widget):
        """Return to the previous image."""
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    def lang_toggle(self, widget, lang):
        """Switch language and reload images."""
        if widget.get_active() and self.language != lang:
            self.language = lang
            self.load_image_paths()
            self.load_image()
    
win = CustomWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
