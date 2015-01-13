
from gi.repository import Gtk, Gio


# python built-in logging 
import logging
logger = logging.getLogger('catgor')
#        logger.debug("Catgor Application")


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(self, title="Catgor", application=app)
        self.set_default_size(600, 400)
		
        grid = Gtk.Grid()
		
        menubutton = Gtk.MenuButton()
        menubutton.set_size_request(80, 35)
        grid.attach(menubutton, 0, 0, 1, 1)
		
        menumodel = Gio.Menu()
        menubutton.set_menu_model(menumodel)
        menumodel.append("Help", "app.help")
        menumodel.append("About", "app.about")
        menumodel.append("Quit", "app.quit")
        		
        self.add(grid)

class CatgorApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        logger.debug("Catgor Application")

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

#        new_action = Gio.SimpleAction.new("new", None)
#        new_action.connect("activate", self.new_callback)
#        self.add_action(new_action)

#        quit_action = Gio.SimpleAction.new("quit", None)
#        quit_action.connect("activate", self.quit_callback)
#        self.add_action(quit_action)



#        self.menu = Gio.Menu()
#        self.menu.append(_("Help"), "app.help")
#        self.menu.append(_("About"), "app.about")
#        self.menu.append(_("Quit"), "app.quit")

#        if session == 'gnome':
#            # Configure GMenu
#            self.set_app_menu(self.menu)

        help_action = Gio.SimpleAction.new("help", None)
        help_action.connect("activate", self.help_cb)
        self.add_action(help_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_cb)
        self.add_action(quit_action)

    def help_cb(self, action, parameter):
        print("You clicked \"Help\"")

    def about_cb(self, action, parameter):
        print("You clicked \"About\"")

    def quit_cb(self, action, parameter):
        print("You clicked \"Quit\"")
        self.quit()
