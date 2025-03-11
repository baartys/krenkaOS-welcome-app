import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

class CustomWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Welcome to KrenkaOS")
        
        # Set the window size to 700x500 and make it unresizable
        self.set_default_size(700, 500)
        self.set_resizable(False)  # Disable window resizing

        # Remove window decoration (no title bar)
        self.set_decorated(False)

        # Set White Background
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        fixed = Gtk.Fixed()
        self.add(fixed)

        # Load and Center the Image
        image = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("tux.png", 217, 200, True)
        image.set_from_pixbuf(pixbuf)
        
        # Centering the Image (Window size: 700x500, Image size: 868x800)
        image_x = (700 - 217) // 2  # Center Horizontally
        image_y = (500 - 200) // 2   # Center Vertically (This will make it partially out of view)
        fixed.put(image, image_x, image_y)

        # Create Buttons
        button1 = Gtk.Button(label="Get Started")
        self.style_button(button1)  # Apply styles
        button1.set_size_request(150, 50)
        button1.connect("clicked", self.close_app)
        fixed.put(button1, 100, 50)  # Positioning manually

        button2 = Gtk.Button(label="Settings")
        self.style_button(button2)
        button2.set_size_request(150, 50)
        fixed.put(button2, 300, 50)

        button3 = Gtk.Button(label="Help")
        self.style_button(button3)
        button3.set_size_request(150, 50)
        fixed.put(button3, 500, 50)

        # Exit Button (Bottom Right)
        exit_button = Gtk.Button(label="Exit")
        self.style_button(exit_button)
        exit_button.set_size_request(100, 40)
        exit_button.connect("clicked", self.close_app)
        fixed.put(exit_button, 580, 450)  # Position exit at bottom right

    def style_button(self, button):
        """Apply custom CSS to buttons"""
        css_provider = Gtk.CssProvider()
        # CSS styles to ensure buttons are orange by default and blue when hovered
        css_provider.load_from_data(f"""
            button {{
                background-color: orange;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
                border: none;  /* Remove default border */
            }}

            button:hover {{
                background-color: blue;
                color: white;
            }}

            button:active {{
                background-color: darkblue; /* Darker blue when clicked */
                color: white;
            }}
        """.encode("utf-8"))

        style_context = button.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def close_app(self, widget):
        Gtk.main_quit()

# Run the App
win = CustomWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
