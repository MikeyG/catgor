from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ValidationError, ParsingError, NoKeyError
from xdg.util import u

import os

SYSTEMAPPS = "/usr/share/applications"
LOCALAPPS = "~/.local/share/applications"

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
                        
