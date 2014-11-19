from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from base import BaseInfo

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
    apps = relationship(
        'DesktopApps', 
        secondary= 'cattoapp'
    )
    categories = Column(String)
    excluded_apps = Column(String)

    def fill_record(self, cat_entry):
        """Fill category data"""

        # clean up the category name        
        self.name = cat_entry.name[0:]

        # Not used right now, but save anyway
        if cat_entry.translate:
            self.translate = True
        else:
            self.translate = False   
    
        # stub
        for tmp in cat_entry.apps:
            try:
                # search for .desktop in DesktopApps
                catsearch = BaseInfo.session.query(
                    DesktopApps).filter(DesktopApps.de_file == tmp).one()
            
            # not in database, so add it
            except NoResultFound:
                catsearch = DesktopApps(de_file=tmp,de_orphan=True)
                BaseInfo.session.add(catsearch)
                BaseInfo.session.commit()
            
            # multi entries if a system and user .desktop are
            # present - user takes priority
            except MultipleResultsFound:
                catsearch = BaseInfo.session.query(
                    DesktopApps).filter(and_(DesktopApps.de_file==tmp,DesktopApps.de_user==True))
                
            finally:
                self.apps.append(catsearch)
                
        # stub        
        if str(cat_entry.categories)[:3] == "@as":
            self.categories = ""
        else:
            self.categories = str(cat_entry.categories)

        # stub
        if str(cat_entry.excluded_apps)[:3] == "@as":
            self.excluded_apps = ""
        else:
            self.excluded_apps = str(cat_entry.excluded_apps)


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
#    de_nodisp = Column(Boolean)
#    de_hidden = Column(Boolean)
    de_onlyshow = Column(String)
    de_notshow = Column(String)
    de_cat = Column(String)
    de_path = Column(String)
    de_gnome_cats = relationship(
        'Categories', 
        secondary= 'cattoapp'
    )
    de_user = Column(Boolean)
    de_orphan = Column(Boolean)

    def fill_record(self, app_entry):
        """Fill application data"""

        self.de_name = app_entry.de_name
        self.de_gname = app_entry.de_gname

        # stub
        for tmp in app_entry.de_onlyshow:
            try:
                onlyshow = BaseInfo.session.query(
                    DisplayManager).filter(DisplayManager.dm_name == tmp).one()
                print "found it"
            except NoResultFound:
                print "Nope"
            except MultipleResultsFound:
                print tmp        

#        for onlyshow in app_entry.de_onlyshow:
#           session.query(Tag).filter(
#                Tag.guid.in_(note.tagGuids),
#            ).all()

#        print self.de_onlyshow



#        self.de_onlyshow = app_entry.de_onlyshow
#        self.de_notshow = app_entry.de_notshow
#        self.de_cat = app_entry.de_cat
        self.de_path = app_entry.de_path 
        self.de_user = app_entry.de_user
        self.de_orphan = app_entry.de_orphan

class DisplayManager(Base):
    __tablename__ = 'dispman'
    id = Column(Integer, primary_key=True)
    dm_name = Column(String)    
    
    
# *************************************************************
# Association tables

class CatToDesktop (Base):
    __tablename__ = 'cattoapp'
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True) 
    
class OnlyshowToDM (Base):
    __tablename__ = 'onlyshow'
    dispman_id = Column(Integer, ForeignKey('dispman.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True)

class NoshowToDM (Base):
    __tablename__ = 'noshow'
    dispman_id = Column(Integer, ForeignKey('dispman.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True)
    
    
