from sqlalchemy import create_engine, __version__ 
from sqlalchemy.orm import sessionmaker

from models import Base
from catgor import APP_STORE

import os

DB_MSG_ECHO = False

# change item to lower case
# used local only
def _nocase_lower(item):
    return unicode(item).lower()

# Setup database
# Ref:  http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
#       http://pypix.com/tools-and-tips/essential-sqlalchemy/
def get_db_session(db_path=None):

    db_path = os.path.expanduser(APP_STORE + "/catgor.db")
    
    print db_path 
    
    # Ex: engine = create_engine('sqlite:///:memory:', echo=True)
    # echo True - logging to python
    # uses mysql-python as the default DBAPI
    engine = create_engine('sqlite:///%s' % db_path, echo=DB_MSG_ECHO)
    Base.metadata.create_all(engine)
    print "got here"

    # creates a factory and assign the name Session    
    Session = sessionmaker(bind=engine)
    session = Session()
    conn = session.connection()
    conn.connection.create_function('lower', 1, _nocase_lower)
    return session

def get_sqlalchemy_version( ):
    return sqlalchemy.__version__
    