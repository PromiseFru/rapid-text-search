import sys, os, logging

logging.basicConfig(level=2)

sys.path.insert(0, '/var/www/home_server/rapid-text-search/')

from main import app as application
