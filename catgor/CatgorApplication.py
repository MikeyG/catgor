
from gi.repository import Gtk, Gio


# python built-in logging 
import logging
logger = logging.getLogger('catgor')

from catgorconst import APP_STORE, VER_MAJOR, VER_MINOR
from catgortools import show_uri


class CatgorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        logger.debug("Catgor ApplicationWindow")
        Gtk.Window.__init__(self, title="Catgor", application=app)
        self.set_default_size(1024, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        		
        grid = Gtk.Grid()
		
        menubutton = Gtk.MenuButton()
        menubutton.set_size_request(80, 35)
        grid.attach(menubutton, 0, 0, 1, 1)
		
        self.add(grid)


class CatgorApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        logger.debug("Catgor Application")

    def do_activate(self):
        logger.debug("do_activate")
        win = CatgorWindow(self)
        win.show_all()

    def do_startup(self):
        logger.debug("do_startup")
        Gtk.Application.do_startup(self)

        # create a menu
        menu = Gio.Menu()

        menu.append("Help", "app.help")        
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")

        # set the menu as menu of the application
        self.set_app_menu(menu)

#        menubutton.set_menu_model(menumodel)
#        self.win.connect('new', self.new_cb)

#        self.win.connect('new', self.new_cb)
#        self.win.connect('about', self.about_cb)
#        self.win.connect('help', self.help_cb)
#        self.win.connect('quit', self.quit_cb)

#        if self.win.app_menu_button:
#            self.win.app_menu_button.set_menu_model(self.menu)
#            self.win.app_menu_button.show_all()


        new_action = Gio.SimpleAction.new("new", None)
        new_action.connect("activate", self.new_cb)
        self.add_action(new_action)

        help_action = Gio.SimpleAction.new("help", None)
        help_action.connect("activate", self.help_cb)
        self.add_action(help_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)
 
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_cb)
        self.add_action(quit_action)

    def new_cb(self, action, parameter):
        print("You clicked \"New\"")

    def help_cb(self, widget, data=None):
        """Help callback function."""
        question = "Do you want to read the Catgor manual online?"
#        dialog = Gtk.MessageDialog(transient_for=self.win, modal=True,
        dialog = Gtk.MessageDialog(modal=True,
                                    message_type=Gtk.MessageType.QUESTION,
                                    buttons=Gtk.ButtonsType.NONE,
                                    text=question)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Read Online", Gtk.ResponseType.OK)
        dialog.set_title("Online Documentation")
        details = "You will be redirected to the documentation website where the help pages are maintained."
        dialog.format_secondary_markup(details)
        if dialog.run() == Gtk.ResponseType.OK:
            help_url = "https://github.com/MikeyG/catgor/wiki"
            logger.debug("Navigating to help page, %s" % help_url)
            #show_uri(self.win, help_url)
        dialog.destroy()

    def about_cb(self, widget, data=None):
        """About callback function.  Display the AboutDialog."""
        
        logger.debug("About dialog")
                
        # Create and display the AboutDialog.
        aboutdialog = Gtk.AboutDialog()

        # Credits
        authors = ["Michael Greene"]
        documenters = ["Michael Greene"]

        # Populate the AboutDialog with all the relevant details.
        aboutdialog.set_title("About Catgor")
        aboutdialog.set_program_name("Catgor")
        aboutdialog.set_version(("%s.%s" % (VER_MAJOR, VER_MINOR)))        
        aboutdialog.set_comments("Gnome overview editor")
#        aboutdialog.set_logo_icon_name("catgor")
        aboutdialog.set_copyright("Copyright \xc2\xa9 2014-2015 Michael Greene")
        aboutdialog.set_authors(authors)
        aboutdialog.set_documenters(documenters)
        aboutdialog.set_website("https://github.com/MikeyG/catgor")
        aboutdialog.set_website_label("Catgor Developer Website")

        # Connect the signal to destroy the AboutDialog when Close is clicked.
        aboutdialog.connect("response", self.about_close_cb)
#        aboutdialog.set_transient_for( Gtk.Window)

        # Show the AboutDialog.
        aboutdialog.show()

    def about_close_cb(self, widget, response):
        """Destroy the AboutDialog when it is closed."""
        widget.destroy()

    def quit_cb(self, widget, data=None):
        """Signal handler for closing the CatgorWindow."""
        self.quit()
