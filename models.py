from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# The declarative_base() callable returns a new base class from 
# which all mapped classes should inherit. When the class definition is 
# completed, a new Table and mapper() will have been generated.
# http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html
Base = declarative_base()

# engine = create_engine('sqlite:///%s' % db_path)
# in tools.py

# *************************************************************
# Categories ORM class to save category specific data to the database
#
# Struct: Categories
#   category - 
#   name -  
#   translate - 
#   apps -
#   categories -
#   excluded_apps -


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    translate = Column(Boolean)
    apps = Column(String)
    categories = Column(String)
    excluded_apps = Column(String)

    def fill_record(self, cat_entry):
        """Fill category data"""

        self.name = cat_entry.name[0:]

        if cat_entry.translate:
            self.translate = True
        else:
            self.translate = False   
             
#        for app_entry in cat_entry.apps:
#            print app_entry

        if str(cat_entry.categories)[:3] == "@as":
            self.categories = ""
        else:
            self.categories = str(cat_entry.categories)

        if str(cat_entry.excluded_apps)[:3] == "@as":
            self.excluded_apps = ""
        else:
            self.excluded_apps = str(cat_entry.excluded_apps)

    def _create_orphan(self, cat_entry):
        pass
       

# *************************************************************
# Desktop_Apps ORM class to save application specific data to the database
#
# Struct: Desktop_Apps
#   de_file - actual .desktop file name
#   de_name - name - Specific name of the application 
#   de_gname - generic name - Generic name of the application 
#   de_nodisp - NoDisplay - NoDisplay means "this application exists, 
#       but don't display it in the menus"
#   de_hidden - Hidden - the user deleted (at his level) something 
#       that was present 
#   de_onlyshow - 
#   de_notshow - 
#   de_cat - List of application categories
#   de_path - full path to application desktop file
#   de_user - True if user file, false if system file
#   de_orphan - .desktop file does not exist in file system
#                but in overview dconf   


class DesktopApps(Base):
    __tablename__ = 'desktop'
    id = Column(Integer, primary_key=True)
    de_file = Column(String)   
    de_name = Column(String)
    de_gname = Column(String)
    de_nodisp = Column(Boolean)
    de_hidden = Column(Boolean)
    de_onlyshow = Column(String)
    de_notshow = Column(String)
    de_cat = Column(String)
    de_path = Column(String)
    de_user = Column(Boolean)
    de_orphan = Column(Boolean)

    def fill_record(self, app_entry):
        """Fill application data"""

        self.de_name = app_entry.de_name
        self.de_gname = app_entry.de_gname
        self.de_nodisp = app_entry.de_nodisp
        self.de_hidden = app_entry.de_hidden
        
#        self.de_onlyshow = []
#        for onlyshow in app_entry.de_onlyshow:
#            self.de_onlyshow.append(onlyshow)
#        print self.de_onlyshow

#        print app_entry.de_onlyshow

        self.de_onlyshow = str(app_entry.de_onlyshow)
#        self.de_notshow = app_entry.de_notshow
#        self.de_cat = app_entry.de_cat
        self.de_path = app_entry.de_path 
        self.de_user = app_entry.de_user
        self.de_orphan = app_entry.de_orphan
