from gi.repository import Gio

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import exc

import models
from base import BaseInfo

# python built-in logging 
import logging
logger = logging.getLogger('catgor')

# Structure to hold category information
class Cat_Struct(object):

    def __init__(self, category, name, translate, apps, 
        categories, excluded_apps
    ):
        self.category = category
        self.name = name
        self.translate = translate
        self.apps = apps
        self.categories = categories
        self.excluded_apps = excluded_apps

      
# ********** Get Categories **********
# 
# Get current category configuration
#
class GetCats(BaseInfo):

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
        
        self._add_entry(self.cat_entry)
        

    # ************** Create Category DB **************
    #
    def _add_entry(self, cat_entry):
        """Add cat entry to database"""

        # create new - models.py 
        cat_record = models.Categories(category=cat_entry.category) 

        # fill in values  
        cat_record.fill_record(cat_entry) 

        #logger.debug("Cat: Created cat record.")        
        
        # add/commit to local database
        self.session.add(cat_record)

        # add/commit to local database
        self.session.add(cat_record)

        try:
            self.session.commit()
        except exc.SQLAlchemyError:
            logger.error("Commit error")


    # will be logger output in future    
    def _print_cat(self, entry):
        print "***********************" + entry.category + "********************"
        print entry.name
        print entry.translate
        print entry.apps
        print entry.categories
        print entry.excluded_apps
