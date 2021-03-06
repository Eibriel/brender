import os
import logging

from flask import Flask
from flask import jsonify
from flask import abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from flask.ext.migrate import Migrate

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from helpers import http_request

try:
    import config
    app.config.from_object(config.Manager)
except ImportError:
    """If a config is not defined, we use the default settings, importing the
    BLENDER_PATH and SETTINGS_PATH from the server.
    """
    server_settings = http_request('localhost:9999', '/settings', 'get')
    app.config.update(
        DEBUG=False,
        HOST='localhost',
        PORT=7777,
        BRENDER_SERVER='localhost:9999',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.path.dirname(__file__), '../task_queue.sqlite'),
        BLENDER_PATH_LINUX=server_settings['blender_path_linux'],
        BLENDER_PATH_OSX=server_settings['blender_path_osx'],
        BLENDER_PATH_WIN=server_settings['blender_path_win'],
        SETTINGS_PATH_LINUX=server_settings['render_settings_path_linux'],
        SETTINGS_PATH_OSX=server_settings['render_settings_path_osx'],
        SETTINGS_PATH_WIN=server_settings['render_settings_path_win']
    )

api = Api(app)


from modules.tasks import TaskManagementApi
from modules.tasks import TaskApi
api.add_resource(TaskManagementApi, '/tasks')
api.add_resource(TaskApi, '/tasks/<int:task_id>')

from modules.workers import WorkerListApi
from modules.workers import WorkerApi
api.add_resource(WorkerListApi, '/workers')
api.add_resource(WorkerApi, '/workers/<int:worker_id>')

@app.errorhandler(404)
def not_found(error):
    response = jsonify({'code' : 404, 'message' : 'No interface defined for URL'})
    response.status_code = 404
    return response
