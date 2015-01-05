
# use same directory as gnome-catgen
APP_STORE = "~/.local/share/applications-categories"

VER_MAJOR = 0 
VER_MINOR = 01

SYSTEMAPPS = "/usr/share/applications"
LOCALAPPS = "~/.local/share/applications"

# http://standards.freedesktop.org/menu-spec/latest/apa.html

# Main Categories
# By including one of the Main Categories in an application's desktop entry file, 
# the application will be ensured that it will show up in a section of the 
# application menu dedicated to this category. If multiple Main Categories are 
# included in a single desktop entry file, the entry may appear more than 
# once in the menu.

# Category-based menus based on the Main Categories listed in this specification 
# do not provide a complete ontology for all available applications. 
# Category-based menu implementations SHOULD therefore provide a "catch-all" 
# submenu for applications that cannot be appropriately placed elsewhere.

# Standard Items
# AudioVideo	Application for presenting, creating, or processing multimedia (audio/video)	 
# Audio			An audio application	Desktop entry must include AudioVideo as well
# Video			A video application	Desktop entry must include AudioVideo as well
# Development	An application for development	 
# Education		Educational software	 
# Game			A game	 
# Graphics		Application for viewing, creating, or processing graphics	 
# Network		Network application such as a web browser	 
# Office		An office type application	 
# Science		Scientific software	 
# Settings		Settings applications	Entries may appear in a separate menu or as part of a "Control Center"
# System		System application, "System Tools" such as say a log viewer or network monitor	 
# Utility		Small utility application, "Accessories"

category_standard = [
    "AudioVideo",
    "Audio",
    "Video",
    "Development",
    "Education",
    "Game",
    "Graphics",
    "Network",
    "Office",
    "Science",
    "Settings",
    "System",
    "Utility"]

# Reserved Categories
# Reserved Categories have a desktop-specific meaning that has not been standardized (yet). 
# Desktop entry files that use a reserved category MUST also include an appropriate 
# OnlyShowIn= entry to restrict themselves to those environments that properly support 
# the reserved category as used.    

# Screensaver	A screen saver (launching this desktop entry should activate the screen saver)
# TrayIcon		An application that is primarily an icon for the "system tray" or "notification area" 
#               (apps that open a normal window and just happen to have a tray icon as well should not list this category)
# Applet		An applet that will run inside a panel or another such application, likely desktop specific
# Shell			A shell (an actual specific shell such as bash or tcsh, not a TerminalEmulator)	 

category_reserved = [
    "Screensaver",
    "TrayIcon",
    "Applet",
    "Shell"]
