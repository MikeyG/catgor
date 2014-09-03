from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound



# The declarative_base() callable returns a new base class from 
# which all mapped classes should inherit. When the class definition is 
# completed, a new Table and mapper() will have been generated.
# http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html
Base = declarative_base()

# engine = create_engine('sqlite:///%s' % db_path)
# in tools.py

# *************************************************************
# Searches ORM class to save data to the database
#


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    translate = Column(Boolean)
    apps = Column(String)
    categories = Column(String)
    excluded_apps = Column(String)

 #   def add_cat(self, savsearch):
 #       """Fill data from api"""
 #       pass

       
class Desktop_Apps(Base):
    __tablename__ = 'desktop'
    id = Column(Integer, primary_key=True)
        




#    def from_api(self, savsearch):
#        """Fill data from api"""





