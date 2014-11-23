from sqlalchemy import create_engine, __version__ 
from sqlalchemy.orm import sessionmaker


from base import BaseInfo
from models import Base
from catgor import APP_STORE

import os

# python built-in logging 
import logging
logger = logging.getLogger('catgor')

DB_MSG_ECHO = False


# Structure to hold category information
class DatabaseInit(object):

    def __init__(self):
        logger.info('Initialize database.')
         
        BaseInfo.db_path = os.path.expanduser(APP_STORE + "/catgor.db")

        # remove old database file        
        try:
            os.remove(BaseInfo.db_path)
        except OSError:
            pass

    # change item to lower case
    # used local only
    def _nocase_lower(item):
        return unicode(item).lower()

    # Setup database
    # Ref:  http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
    #       http://pypix.com/tools-and-tips/essential-sqlalchemy/
    def get_db_session(self):
    	
        logger.debug('get_db_session start')

        # Ex: engine = create_engine('sqlite:///:memory:', echo=True)
        # echo True - logging to python
        # uses mysql-python as the default DBAPI
        engine = create_engine('sqlite:///%s' % BaseInfo.db_path, echo=DB_MSG_ECHO)
        Base.metadata.create_all(engine)

        # creates a factory and assign the name Session    
        Session = sessionmaker(bind=engine)
        session = Session()
#        conn = session.connection()
#        conn.connection.create_function('lower', 1, _nocase_lower)
        BaseInfo.session = session
        
        logger.debug('get_db_session finish')

    # return sql version
    def get_sqlalchemy_version(self):
        return __version__
    