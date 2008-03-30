import os, sys
from os.path import join, exists, isdir, isfile, dirname, abspath, expanduser
from shutil import copy as copyfile

import gtk, gnome.ui
from gtk import glade
import gettext
import locale

# Autotools set the actual data_dir in defs.py
from db import Storage
from defs import *
from dispatcher import Dispatcher

# Init i18n
import __builtin__
__builtin__._ = gettext.gettext

# Allow to use not installed hamster
UNINSTALLED_HAMSTER = False
def _check(path):
    return exists(path) and isdir(path) and isfile(path+"/AUTHORS")

name = join(dirname(__file__), '..')
if _check(name):
    UNINSTALLED_HAMSTER = True

# Sets SHARED_DATA_DIR to local copy, or the system location
# Typically shared data dir is /usr/share/hamster-applet
if UNINSTALLED_HAMSTER:
    SHARED_DATA_DIR = abspath(join(dirname(__file__), '..', 'data'))
else:
    SHARED_DATA_DIR = join(DATA_DIR, "hamster-applet")
print "Data Dir: %s" % SHARED_DATA_DIR

USER_HAMSTER_DIR = expanduser("~/.gnome2/hamster-applet")
DB_FILE = 'hamster.db'
HAMSTER_DB = join(USER_HAMSTER_DIR, DB_FILE)
if not exists(USER_HAMSTER_DIR):
    try:
        os.makedirs(USER_HAMSTER_DIR, 0744)
    except Exception , msg:
        print 'Error:could not create user dir (%s): %s' % (USER_HAMSTER_DIR, msg)

#check if db is here
if not exists(HAMSTER_DB):
    print "Database not found in %s - installing default from %s!" % (HAMSTER_DB, SHARED_DATA_DIR)
    copyfile(join(SHARED_DATA_DIR, DB_FILE), HAMSTER_DB)

# Init storage

dispatcher = Dispatcher()
storage = Storage(dispatcher)
    
# Path to images, icons
ART_DATA_DIR = join(SHARED_DATA_DIR, "art")

