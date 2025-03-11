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
        def load_css(self):
            """Load and apply external CSS to the entire window"""
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path('styles.css')  # Load external CSS file

            # Apply CSS to the entire screen context with user priority
            Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)  # Try using STYLE_PROVIDER_PRIORITY_USER
        # Create a fixed layout container
        fixed = Gtk.Fixed()
        self.add(fixed)

        # Load and apply the CSS styles from the external file
        self.load_css()

        # Load and center the Image
        image = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("tux.png", 217, 200, True)
        image.set_from_pixbuf(pixbuf)
        
        # Centering the Image (Window size: 700x500, Image size: 868x800)
        image_x = (700 - 217) // 2  # Center Horizontally
        image_y = (500 - 200) // 2   # Center Vertically (This will make it partially out of view)
        fixed.put(image, image_x, image_y)


        # Create and position Button
        button1 = Gtk.Button(label="Next")
        button1.set_size_request(100, 20)
        button1.connect("clicked", self.close_app)
        fixed.put(button1, 595, 5)  # Positioning manually

    def load_css(self):
        """Load and apply external CSS to the entire window"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('styles.css')  # Load external CSS file
        
        # Apply CSS to the entire screen context
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def close_app(self, widget):
        Gtk.main_quit()

# Run the App
win = CustomWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
