from gi.repository import Gio 
from sqlalchemy import create_engine

from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ValidationError, ParsingError, NoKeyError
from xdg.util import u

import os

SYSTEMAPPS = "/usr/share/applications"
LOCALAPPS = "~/.local/share/applications"
APP_STORE = "~/.local/share/applications-categories"

# Structure to hold category information
class Cat_Struct(object):

    def __init__(self, key, name, translate, apps, 
        categories, excluded_apps
    ):
        self.key = key
        self.name = name
        self.translate = translate
        self.apps = apps
        self.categories = categories
        self.excluded_apps = excluded_apps


# Structure to hold .desktop entry information      
class Desktop_Entry(object):

    def __init__(self, de_name, de_gname, de_nodisp, de_hidden,
         de_onlyshow, de_notshow, de_cat, de_path
    ): 

        self.de_name = de_name
        self.de_gname = de_gname
        self.de_nodisp = de_nodisp
        self.de_hidden = de_hidden
        self.de_onlyshow = de_onlyshow
        self.de_notshow = de_notshow
        self.de_cat = de_cat
        self.de_path = de_path      
      
      
# ********** Get Categories **********
# 
# Get current category configuration
#
class GetCats( ):

    categories = []
    dconf_cats = Gio.Settings("org.gnome.desktop.app-folders")
 
    def __init__(self):
       pass

    def get_categories(self):

        # Get the current overview categories        
        categories = self._get_categories_list( )
        
        # to be removed
        print categories

        for folder in categories:
          self._get_folder_entry(folder)
         
    # *** _get_categories(self) - local
    # get categories using gsettings - folder-children
    # Should be at least set to [] on default install 
    def _get_categories_list(self):
        categories=self.dconf_cats.get_value("folder-children")
        return categories

    # *** _get_folder_entry(self, category) - local   
    # Read the keys related to the provided category store in CatStruct
    # 'translate', 'categories', 'apps', 'excluded-apps', 'name'
    def _get_folder_entry(self, category):
        cat_data = Gio.Settings.new_with_path("org.gnome.desktop.app-folders.folder", 
            "/org/gnome/desktop/app-folders/folders/%s/" % (category))
        self.cat_entry = Cat_Struct(
            category,
            cat_data.get_value('name'),
            cat_data.get_value('translate'),
            cat_data.get_value('apps'),
            cat_data.get_value('categories'),
            cat_data.get_value('excluded-apps')
        )      
        # this will be debug in future
        self._print_cat(self.cat_entry)
        # will call to fill in orm database future

    # will be logger output in future    
    def _print_cat(self, entry):
        print "***********************" + entry.key + "********************"
        print entry.name
        print entry.translate
        print entry.apps
        print entry.categories
        print entry.excluded_apps

        
# ********** Get Desktop Entry **********
# 
# Get desktop entry data
#
class AppList( ):

    def __init__(self):
        pass

    def get_desktop(self):
        self._get_app_list(SYSTEMAPPS)
        self._get_app_list(LOCALAPPS)

    # *** _get_app_list
    # Takes a desktop entry directory and uses xdg module to pull in
    # all the data needed and stores in Desktop_Entry structure.
    def _get_app_list(self, directory):
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".desktop"):
                     app_path = root + "/" + name
                     xgd_de = DesktopEntry(app_path)
                     self.app_entry = Desktop_Entry(
                         xgd_de.getName( ),
                         xgd_de.getGenericName( ),
                         xgd_de.getNoDisplay( ),
                         xgd_de.getHidden( ),
                         xgd_de.getOnlyShowIn( ),
                         xgd_de.getNotShowIn( ),
                         xgd_de.getCategories( ),
                         app_path
                     )
                     # this will be debug in future
                     self._print_app(self.app_entry)
                     # will call to fill in orm database future

    # will be logger output in future    
    def _print_app(self, entry):
        print "********************************************"
        print entry.de_name
        print entry.de_gname
        print entry.de_nodisp 
        print entry.de_hidden
        print entry.de_onlyshow
        print entry.de_notshow
        print entry.de_cat
        print entry.de_path
                        


if __name__ == "__main__":

    try:
        os.mkdir(APP_STORE)
    except OSError:
        pass	
	

    GetCats( ).get_categories( )
    AppList( ).get_desktop( )
    


    
    
    
    

    