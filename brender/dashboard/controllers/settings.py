import json
from flask import (flash,
                   render_template,
                   request,
                   Blueprint)

from dashboard import app
from dashboard import http_server_request, list_integers_string, check_connection

# Name of the Blueprint
settings = Blueprint('settings', __name__)


@settings.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        params = request.form
        http_server_request('post', '/settings', params)

    projects = http_server_request('get', '/projects')
    settings = http_server_request('get', '/settings')
    return render_template('settings/index.html',
                           title='settings',
                           settings=settings,
                           projects=projects)


@settings.route('/render/', methods=['GET'])
def render():
    render_settings = http_server_request('get', '/settings/render')
    return render_template('settings/render.html',
                           title='render settings',
                           render_settings=render_settings)


@settings.route('/status/', methods=['GET'])
def status():
    try:
        server_status = check_connection()
        server_stats = http_server_request('get', '/stats')
    except:
        server_status = 'offline'
        server_stats = ''
    return render_template('settings/status.html',
        title='server status',
        server_stats=server_stats,
        server_status=server_status)
