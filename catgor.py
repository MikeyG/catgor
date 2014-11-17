from dbus.mainloop.glib import DBusGMainLoop

import os
import signal

# python built-in logging 
import logging

import tools 

from base import BaseInfo

from applist import AppList
from catlist import GetCats

# use same directory as gnome-catgen
APP_STORE = "~/.local/share/applications-categories"


def _start_logging(verbose):


    # ************************************************************
    #                   Configure logger
    # ************************************************************
    # https://docs.python.org/2/library/logging.html
    # good ref: 
    # http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
    # Yes, quite drawn out with all my if verbose, but readable for me when 
    # I come back to this in a couple weeks or more

    #logging.basicConfig(level=logging.INFO)
        
    # create logger and set to debug
    logger = logging.getLogger('catgor')
    logger.setLevel(logging.DEBUG)
       
    fh = logging.FileHandler(
        os.path.expanduser(APP_STORE+"/catgor.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter( 
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    if verbose:
        ch = logging.StreamHandler( )
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(ch)

    logger.info('Logging started.')


# creates directories - called from main( )
def _create_dirs( ):
    """Create dirs"""
    try:
        os.mkdir(APP_STORE)
    except OSError:
        pass
 

# kicks things off 
def main( ):
    # ctrl-c terminates the process gracefully
    # http://docs.python.org/dev/library/signal.html
    # http://pymotw.com/2/signal/
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # create directories - _create_dirs local
    _create_dirs( )

    # call to start logging
    _start_logging("TRUE")
    logger = logging.getLogger('catgor')

    # Setup database for use    
    dbsession = tools.DatabaseInit( )    
    logger.info("sqlalchemy version %s" % dbsession.get_sqlalchemy_version( )) 
    logger.info("DB Path %s" % BaseInfo.db_path)
    dbsession.get_db_session( )

    AppList( ).get_desktop( ) 

    # Get current overview configuration and insert into database
    GetCats( ).get_categories(BaseInfo.session)
           


if __name__ == "__main__":

    main( )


    


    
    
    
    

    