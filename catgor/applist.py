#   Catgor - Gnome 3 Overview category editor
#   Copyright (C) 2014-2015 Michael Greene <mikeos2@gmail.com>
#
#   Some parts used from:
#   MenuLibre - Advanced fd.o Compliant Menu Editor
#   Copyright (C) 2012-2014 Sean Davis <smd.seandavis@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License version 3, as published
#   by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranties of
#   MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.

from xdg.DesktopEntry import DesktopEntry
from xdg.Exceptions import ValidationError, ParsingError, NoKeyError
from xdg.util import u

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import exc

import os

import models
from catgorbase import BaseInfo

# python built-in logging 
import logging
logger = logging.getLogger('catgor')

from catgorconst import SYSTEMAPPS, LOCALAPPS

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

                        
