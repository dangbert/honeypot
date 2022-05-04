#!/usr/bin/env python3
# running this file will start the app (execute app/__init__.py)

import os, sys
from app import create_app, getConfigForEnv

def getApp():
    return create_app(getConfigForEnv())

if __name__ == "__main__":
    app = getApp()
    host = None
    if len(sys.argv) > 1:
        host = sys.argv[1] # option to specify host IP (for dev docker)
        print('running with host: ' + host)
    app.run(host=host) # start on localhost:5000
else:
    # for uWSGI (which needs to be able to import app) https://stackoverflow.com/a/12030880
    app = getApp()
