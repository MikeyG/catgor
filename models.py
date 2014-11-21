from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, and_
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
    categories = relationship(
        'CategoryList', 
        secondary= 'cattocats'
    )    
    excluded_apps = relationship(
        'DesktopApps', 
        secondary= 'cattoexclude'
    )


    def fill_record(self, cat_entry):
        """Fill category data"""

        # clean up the category name        
        self.name = cat_entry.name[0:]

        # Not used right now, but save anyway
        if cat_entry.translate:
            self.translate = True
        else:
            self.translate = False   

        # handle categories apps    
        for tmp in cat_entry.apps:
            # search for .desktop app, all apps should be in  DesktopApps
            # by this point	
            try:
                catapp = BaseInfo.session.query(
                    DesktopApps).filter(DesktopApps.de_file==tmp).one()
                        
            # we get here because an app (.desktop) exists in system and
            # user directory, so query again and get user .desktop            
            except MultipleResultsFound:
                catapp = BaseInfo.session.query(
                    DesktopApps).filter(and_(DesktopApps.de_file==tmp,
                        DesktopApps.de_user==True)).one()                        
            
            # add to to table via association table CatToDesktop
            self.apps.append(catapp)

        # handle categories in each category    
        for tmp in cat_entry.categories:
            # search 	
            catcats = BaseInfo.session.query(
                CategoryList).filter(CategoryList.cat_name==tmp).one()
            
            # add to to table via association table CatToCats
            self.apps.append(catcats)
                
        # handle excluded apps in each category    
        for tmp in cat_entry.excluded_apps:
            # search 	
            exapps = BaseInfo.session.query(
                DesktopApps).filter(DesktopApps.de_file==tmp).one()
            
            # add to to table via association table CatToExclude
            self.apps.append(exapps)


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
    de_onlyshow = relationship(
        'DisplayManager', 
        secondary= 'onlyshow'
    )
    de_notshow = relationship(
        'DisplayManager', 
        secondary= 'noshow'
    )
    de_cat = relationship(
        'CategoryList', 
        secondary= 'apptocats'
    )
    de_path = Column(String)
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
                print "nope"
            except MultipleResultsFound:
                print "double nope"        

#        self.de_onlyshow = app_entry.de_onlyshow
#        self.de_notshow = app_entry.de_notshow
#        self.de_cat = app_entry.de_cat
        self.de_path = app_entry.de_path 
        self.de_user = app_entry.de_user
        self.de_orphan = app_entry.de_orphan

# ************************************************************
# Table to hold category names from both overview categories
# and .desktop categories

class CategoryList(Base):
    __tablename__ = 'catlist'
    id = Column(Integer, primary_key=True)
    cat_name = Column(String) 
 
    
# ************************************************************
# Table to hold .desktop display manager names

class DisplayManager(Base):
    __tablename__ = 'dispman'
    id = Column(Integer, primary_key=True)
    dm_name = Column(String)    
    
    
# *************************************************************
# Association tables:
#   - CatToDesktop - overview groups (category) to .desktop (apps) 
#       which are already assigned
#
#   - DesktopToCat - .desktop (app) assigned categories
#
#   - 

# association table category apps to include
class CatToDesktop (Base):
    __tablename__ = 'cattoapp'
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True) 

# association table category categories to include
class CatToCats (Base):
    __tablename__ = 'cattocats'
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True) 

# association table category excluded apps
class CatToExclude (Base):
    __tablename__ = 'cattoexclude'
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True) 

class AppsToCats (Base):
    __tablename__ = 'apptocats'
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
        
class OnlyshowToDM (Base):
    __tablename__ = 'onlyshow'
    dispman_id = Column(Integer, ForeignKey('dispman.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True)

class NoshowToDM (Base):
    __tablename__ = 'noshow'
    dispman_id = Column(Integer, ForeignKey('dispman.id'), primary_key=True)
    desktop_id  = Column(Integer, ForeignKey('desktop.id'), primary_key=True)
    

#*************************************************************
#  Add the current category .desktop apps to DesktopApps
# 
def cat_apps(cat_entry):
    """Fill application data"""        

    # Add Category .desktop entries to DesktopApps
    for tmp in cat_entry.apps:
        try:
            # search for .desktop in DesktopApps
            catsearch = BaseInfo.session.query(
                DesktopApps).filter(DesktopApps.de_file == tmp).one()
            
        # not in database, so add it as an orphan
        except NoResultFound:
            catsearch = DesktopApps(de_file=tmp,de_orphan=True)
            BaseInfo.session.add(catsearch)
            BaseInfo.session.commit()
            
        # multi entries if a system and user .desktop are
        # present 
        except MultipleResultsFound:
            # do nothing, sort it out later            
            pass

#*************************************************************
#  Add the current category .desktop apps to CategoryList
# 
def cat_list(cat_list):
    """Fill category list """ 

    for tmp in cat_list:
       
        try:
            # search for categories in DesktopApps
            listcats = BaseInfo.session.query(CategoryList).filter(CategoryList.cat_name == tmp).one()
            
        # not in database, so add it 
        except NoResultFound:
            listcats = CategoryList(cat_name=tmp)
            BaseInfo.session.add(listcats)
            BaseInfo.session.commit()

#*************************************************************
#  Add the current category .desktop apps to DesktopApps
# 
                
def dm_list(dm_entry):
    """Fill display manager list """ 
    
    for tmp in dm_entry:
        try:
            # search for dm in DisplayManager
            dmlist = BaseInfo.session.query(
                DisplayManager).filter(DisplayManager.dm_name == tmp).one()
            
        # not in database, so add it 
        except NoResultFound:
            dmlist = DisplayManager(dm_name=tmp)
            BaseInfo.session.add(dmlist)
            BaseInfo.session.commit()             
                
