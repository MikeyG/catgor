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

from sqlalchemy import create_engine, __version__ 
from sqlalchemy.orm import sessionmaker

import os

# python built-in logging 
import logging
logger = logging.getLogger('catgor')

from models import Base

# sqlalchemy debug
#DB_MSG_ECHO = True
DB_MSG_ECHO = False

# change item to lower case
# used local only
def _nocase_lower(item):
    return unicode(item).lower()

# Setup database
# Ref:  http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
#       http://pypix.com/tools-and-tips/essential-sqlalchemy/
def get_db_session(db_path):
    	
    logger.debug('get_db_session start')

    # Ex: engine = create_engine('sqlite:///:memory:', echo=True)
    # echo True - logging to python
    engine = create_engine('sqlite:///%s' % db_path, echo=DB_MSG_ECHO)
    Base.metadata.create_all(engine)
                
    # creates a factory and assign the name Session        
    Session = sessionmaker(bind=engine)
    session = Session()

    conn = session.connection()
    conn.connection.create_function('lower', 1, _nocase_lower)

    logger.debug('get_db_session finish')

    return session

# return sql version
def get_sqlalchemy_version( ):
    return __version__
    

def get_builder(builder_file_name):
    """Return a fully-instantiated Gtk.Builder instance from specified ui
    file

    :param builder_file_name: The name of the builder file, without extension.
        Assumed to be in the 'ui' directory under the data path.
    """
    # Look for the ui file that describes the user interface.
    ui_filename = get_data_file('ui', '%s.ui' % (builder_file_name,))
    if not os.path.exists(ui_filename):
        ui_filename = None

    builder = Gtk.Builder()
    builder.add_from_file(ui_filename)
    builder.set_translation_domain('menulibre')
    builder.add_from_file(ui_filename)
    return builder
    

