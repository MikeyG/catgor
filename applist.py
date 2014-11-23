from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ValidationError, ParsingError, NoKeyError
from xdg.util import u

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import exc

import os

import models
from base import BaseInfo

# python built-in logging 
import logging
logger = logging.getLogger('catgor')

SYSTEMAPPS = "/usr/share/applications"
LOCALAPPS = "~/.local/share/applications"

# Structure to hold .desktop entry information      
class Desktop_Entry(object):

    def __init__(self, de_file, de_name, de_gname, de_nodisp, de_hidden,
         de_onlyshow, de_notshow, de_cat, de_path, de_user, de_orphan
    ): 
        self.de_file = de_file           # desktop filename
        self.de_name = de_name
        self.de_gname = de_gname
        self.de_nodisp = de_nodisp
        self.de_hidden = de_hidden
        self.de_onlyshow = de_onlyshow
        self.de_notshow = de_notshow
        self.de_cat = de_cat
        self.de_path = de_path   
        self.de_user = de_user           # user directory or system
        self.de_orphan = de_orphan       # orphan if only in config
        

# ********** Get Desktop Entry **********
# 
# Get desktop entry data
#
class AppList( ):

    def __init__(self):
        pass

    def get_desktop(self):
       
        logger.info("Process system desktop")
        self._get_app_list(os.path.expanduser(SYSTEMAPPS), False)

        logger.info("Process user desktop")
        self._get_app_list(os.path.expanduser(LOCALAPPS), True)

    # *** _get_app_list
    # Takes a desktop entry directory and uses xdg module to pull in
    # all the data needed and stores in Desktop_Entry structure.
    def _get_app_list(self, directory, user):
        for root, dirs, files in os.walk(directory):
            for name in files:
                if name.endswith(".desktop"):
                  
                    app_path = root + "/" + name
                    
                    # setup desktop entry to access its elements                    
                    xgd_de = DesktopEntry(app_path)
                    
                    #                    
                    self.app_entry = Desktop_Entry(
                        name,
                        xgd_de.getName( ),
                        xgd_de.getGenericName( ),
                        xgd_de.getNoDisplay( ),
                        xgd_de.getHidden( ),
                        xgd_de.getOnlyShowIn( ),
                        xgd_de.getNotShowIn( ),
                        xgd_de.getCategories( ),
                        app_path,
                        user,
                        False
                    )   
                     
                    # Just as a note, skip no display or hidden .desktop                    
                    if not (self.app_entry.de_nodisp or self.app_entry.de_hidden):
                        self._add_entry(self.app_entry)                        


    # ************** Create Application DB **************
    #
    def _add_entry(self, app_entry):
        """Add app entry to database"""

        # run through and categories to database
        models.cat_list(app_entry.de_cat)
        
        # add display managers to database
        models.dm_list(app_entry.de_onlyshow)
        models.dm_list(app_entry.de_notshow)
                
        # create new - models.py 
        app_record = models.DesktopApps(de_file=app_entry.de_file) 

        # fill in values  
        app_record.fill_record(app_entry) 

        # add/commit to local database
        BaseInfo.session.add(app_record)

        try:
            BaseInfo.session.commit( )
        except exc.SQLAlchemyError:
            logger.error("Commit error")

                        
