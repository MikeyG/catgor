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

import optparse
import sys
import os
import signal

# python built-in logging 
import logging
import argparse

from catgorconst import APP_STORE, VER_MAJOR, VER_MINOR
import catgortools 
from catgorbase import BaseInfo
from applist import AppList
from catlist import GetCats

from models import dump_apps, dump_cats

# ************************************************************
#                   Configure logger
# ************************************************************
# https://docs.python.org/2/library/logging.html
# good ref: 
# http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
# Yes, quite drawn out with all my if verbose, but readable for me when 
# I come back to this in a couple weeks or more

def _start_logging(verbose, debug):
    """Catgor logger setup"""
        
    # create logger and set level
    logger = logging.getLogger('catgor')
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
		logger.setLevel(logging.INFO)
       
    fh = logging.FileHandler(
        os.path.expanduser(APP_STORE+"/catgor.log"))

    if debug:
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)
        		
    fh.setFormatter(logging.Formatter( 
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    if verbose:
        ch = logging.StreamHandler( )
        if debug:
			ch.setLevel(logging.DEBUG)
        else:
			ch.setLevel(logging.INFO)			
			
        ch.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.addHandler(ch)

    logger.info('Logging started.')


# creates directories - called from main( ) create app 
# directory if needed
def _create_dirs( ):
    """Create dirs"""

    try:
        os.mkdir(APP_STORE)
    except OSError:
        pass

# deletes old backup and renames existing catgor.db to
# catgor.bak
def _backup_db(logger):
    """Backup current database"""

    logger.debug("Backup database")

    # remove old backup
    try:
        os.remove(os.path.expanduser(APP_STORE + "/catgor.bak"))
    except OSError:
		pass

    # backup
    try:
		os.rename(BaseInfo.db_path,
		    os.path.expanduser(APP_STORE + "/catgor.bak"))
    except OSError:
        pass


def main():
    """Main application for Catgor"""

    # ctrl-c terminates the process gracefully
    # http://docs.python.org/dev/library/signal.html
    # http://pymotw.com/2/signal/
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # create directory if needed - _create_dirs local
    _create_dirs()
    
    # parse args using funky python built-in stuff
    # ref: http://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser(description='Catgor start options.')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('-i', '--initialize', action='store_true', help='initialize database current configuration')
    parser.add_argument('-s', '--spec', action='store_true', help='start with empty database and spec categories')
    parser.add_argument('-d', '--debug', action='store_true', help='debug output')
    parser.add_argument('-V', '--version', action='store_true', help='show version')
    args = parser.parse_args(sys.argv[1:])
    
    # print version and exit, executes sys.exit(0)
    if args.version:
		print 'Catgor version: %s.%s' % (VER_MAJOR, VER_MINOR)
		sys.exit(0)

    # catch use of both -i and -s 
    if (args.initialize and args.spec):
		print "ERROR: Use only -i or -s flags, not both"
		parser.print_help()
		sys.exit(0)
		        
    # if debug set then verbose should be true
    if args.debug:
		args.verbose = 'True'  

    # call to start logging
    _start_logging(args.verbose,args.debug)
    logger = logging.getLogger('catgor')
    
    # yep - current version
    logger.debug("Catgor version: %s.%s" % (VER_MAJOR, VER_MINOR))

    # path to database
    BaseInfo.db_path = os.path.expanduser(APP_STORE + "/catgor.db")

    # check for existing database
    if os.path.isfile(BaseInfo.db_path):
	logger.debug("Found existing database")
    
        # backup current database
        _backup_db(logger) 
    else:
        # if no database and -i or -s not specified then
        # we need to initialize
        logger.debug("Existing database not found")
        if not (args.initialize or args.spec):
            args.initialize = 'True'

    # remove old database file for initialize or spec
    if (args.initialize or args.spec):
        logger.debug("Delete current database")
        try:
            os.remove(BaseInfo.db_path)
        except OSError:
            pass

    # Setup database for use    
    dbsession = catgortools.DatabaseInit( )    
    logger.info("sqlalchemy version %s" % dbsession.get_sqlalchemy_version( )) 
    logger.info("DB Path %s" % BaseInfo.db_path)
    dbsession.get_db_session( )

    if (args.initialize or args.spec):
        # collect all the desktop entries 
        AppList( ).get_desktop( )

        if args.spec:
            logger.debug('Initialize database to specification.')
        
        elif args.initialize:
            logger.debug('Initialize database to current.')
	    
            # Get current overview configuration and insert into database
            GetCats( ).get_categories( )

    dump_cats( )
    dump_apps( )     



    # Run the application.
#    app = CatgorApplication.Application()
#    exit_status = app.run(None)
#    sys.exit(exit_status)

    

