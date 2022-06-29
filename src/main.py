print(__file__)

from gevent import monkey

monkey.patch_all()

from app import create_app

import os

main = create_app(os.getenv('FLASK_CONFIG') or 'default')
