from gi.repository import Gio

#from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
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
class GetCats( ):

    categories = []
    dconf_cats = Gio.Settings("org.gnome.desktop.app-folders")
 
    def __init__(self):
       pass

    def get_categories(self, session):

        logger.debug('get_categories start')

        # Get the current overview categories        
        categories = self._get_categories_list( )

        for category in categories:
            logger.debug('Category: %s' % category)       
            self._get_folder_entry(category)

        logger.debug('get_categories done')
         
    # *** _get_categories(self) - local
    # get categories using gsettings - folder-children
    # Should be at least set to [] on default install 
    def _get_categories_list(self):

        logger.info("Process system categories")
        logger.debug('_get_categories_list')

        categories=self.dconf_cats.get_value("folder-children")
        return categories

    # *** _get_folder_entry(self, category) - local   
    # Read the keys related to the provided category store in CatStruct
    # 'translate', 'categories', 'apps', 'excluded-apps', 'name'
    def _get_folder_entry(self, category):
    	
        # new_with_path(schema_id: String, path: String)    	
        cat_data = Gio.Settings.new_with_path("org.gnome.desktop.app-folders.folder", 
            "/org/gnome/desktop/app-folders/folders/%s/" % (category))
            
        # http://wiki.gentoo.org/wiki/Gnome_Applications_Folders
        #
        # /usr/share/glib-2.0/schemas        
        # org.gnome.desktop.app-folders.gschema.xml
            
        self.cat_entry = Cat_Struct(
            category,
            cat_data.get_value('name'),
            cat_data.get_value('translate'),
            cat_data.get_value('apps'),
            cat_data.get_value('categories'),
            cat_data.get_value('excluded-apps')
        )

        # if no categories then empty field
        if str(self.cat_entry.categories)[:3] == "@as":
            self.cat_entry.categories = ""
            
        # if no excluded then empty field
        if str(self.cat_entry.excluded_apps)[:3] == "@as":
            self.cat_entry.excluded_apps = "" 
        
        self._add_entry(self.cat_entry)      

        
    # ************** Create Category DB **************
    #
    def _add_entry(self, cat_entry):
        """Add cat entry to database"""

        # run through category apps and add orphans to Desktop
        # database, add DM and categories to database
        models.cat_apps(cat_entry)

        # run through and categories to database
        models.cat_list(cat_entry.categories)

        # create new - models.py 
        cat_record = models.Categories(category=cat_entry.category) 

        # fill in values  
        cat_record.fill_record(cat_entry) 

 #       logger.debug("Cat: Created cat record.")        
        
        # add/commit to local database
        BaseInfo.session.add(cat_record)

        try:
            BaseInfo.session.commit( )
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

