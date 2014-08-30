from sqlalchemy import create_engine

import os

from applist import AppList
from catlist import GetCats

APP_STORE = "~/.local/share/applications-categories"




if __name__ == "__main__":

    try:
        os.mkdir(APP_STORE)
    except OSError:
        pass	
	

    GetCats( ).get_categories( )
    AppList( ).get_desktop( )
    


    
    
    
    

    