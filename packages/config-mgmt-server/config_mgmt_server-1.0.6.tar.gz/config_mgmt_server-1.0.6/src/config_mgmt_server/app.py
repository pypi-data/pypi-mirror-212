# save this as app.py
from flask import Flask
from celery import current_app
from celery.bin import worker

worker = worker.worker(app=current_app)

class config_mgmt_server:
    app = Flask(__name__)
    
    # constructor function    
    def __init__(self, name = ""):
        self.name = name
        app = current_app._get_current_object()
        options = {
            'broker': 'redis://localhost:6379/0',
            'loglevel': 'INFO',
            'traceback': True,
        }
        worker.run(**options)
        app.run()

    @app.route("/")
    def hello(self):
        return "Hello, World!"

# Make sure there is a newline at the bottom!
