import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

class CustomWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to KrenkaOS")
        self.set_default_size(700, 500)
        self.set_resizable(True)
        self.set_decorated(False)

        # List of images (non-cyclic navigation)
        self.image_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tux.png'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slide1.png')
        ]
        self.current_image_index = 0

        # Create a fixed layout container
        self.fixed = Gtk.Fixed()
        self.add(self.fixed)

        # Load CSS
        self.load_css()

        # Create an EventBox to wrap the image for custom background styling
        # Create an EventBox to wrap the image for custom background styling
        self.image_event_box = Gtk.EventBox()
        self.image_event_box.set_visible_window(True)  # Enable drawing of background and border
        self.image_event_box.set_name("image_box")
        self.fixed.put(self.image_event_box, 0, 0)


        # Create the Gtk.Image widget
        self.image = Gtk.Image()
        self.image_event_box.add(self.image)

        # Load and display the initial image
        self.load_image()

        # Create and position the Next button
        self.button_next = Gtk.Button(label="Next")
        self.button_next.set_size_request(100, 40)
        self.button_next.connect("clicked", self.next_click)
        self.fixed.put(self.button_next, 590, 10)
        
        # Create and position the Previous button
        self.button_prev = Gtk.Button(label="Previous")
        self.button_prev.set_size_request(100, 40)
        self.button_prev.set_name("previous_button")
        self.button_prev.connect("clicked", self.prev_click)
        self.button_prev.hide()
        self.fixed.put(self.button_prev, 10, 10)
        
        # Create and position the label
        label_krenka = Gtk.Label(label="KrenkaOS LTS")
        label_krenka.set_name("krenka_label")
        label_krenka.set_xalign(0.5)
        label_krenka.set_yalign(0.5)
        self.fixed.put(label_krenka, 265, 10)

        # Connect the resize event to re-center the image
        self.connect("configure-event", self.on_resize)

        # Update buttons visibility for the first image
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

    def load_image(self):
        """Load and center the image while resizing to fit the window, and update background if needed."""
        img_path = self.image_paths[self.current_image_index]
        
        try:
            # Get the current size of the window
            window_width, window_height = self.get_size()
            print(f"Window size: {window_width}x{window_height}")

            # Default values for image dimensions
            image_width = image_height = 0

            # If it's the Tux image (fixed size: 217x200)
            if "tux.png" in img_path:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 217, 200, True)
                self.image.set_from_pixbuf(pixbuf)
                image_width, image_height = 217, 200
                # Update the event box style if needed (e.g., remove custom background)
                self.image_event_box.get_style_context().remove_class("slide-background")
            
            # If it's the slide image (scaled to fit)
            elif "slide1.png" in img_path:
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
                # Add the custom CSS class for the border
                self.image_event_box.get_style_context().add_class("slide-background")

            # Center the image_event_box (and thus the image)
            image_x = (window_width - image_width) // 2
            image_y = (window_height - image_height) // 2
            self.fixed.move(self.image_event_box, image_x, image_y)

        except Exception as e:
            print(f"Error loading image: {e}")

    def update_buttons(self):
        """Update visibility of Next/Previous buttons based on current_image_index."""
        if self.current_image_index == 0:
            self.button_prev.hide()
            self.button_next.show()
        elif self.current_image_index == len(self.image_paths) - 1:
            self.button_next.hide()
            self.button_prev.show()
        else:
            self.button_next.show()
            self.button_prev.show()

    def on_resize(self, widget, event):
        self.load_image()

    def next_click(self, widget):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_image()
            self.update_buttons()

    def prev_click(self, widget):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()
            self.update_buttons()

    def close_app(self, widget):
        Gtk.main_quit()

win = CustomWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
