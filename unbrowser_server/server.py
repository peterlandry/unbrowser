import os
import subprocess
import uuid
from functools import wraps

from flask import Flask, request, url_for, abort, jsonify, render_template

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('auth.cfg', silent=True)


def check_auth(username, password):
    return username == app.config['UNBROWSER_USERNAME'] and password == app.config['UNBROWSER_PASSWORD']


def authenticate(message):
    message = {'message': message}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate("Authenticate")

        elif not check_auth(auth.username, auth.password):
            return authenticate("Authentication Failed.")
        return f(*args, **kwargs)

    return decorated


def _param(name, default=None):
    """ Safely get a parameter, return default if not found """
    return request.form.get(name, default)


@app.route('/webkit/casper/', methods=['POST'])
@requires_auth
def casper():
    js_script = _param('js_script')  # the casperjs script to run for this request

    if not js_script:
        abort(400, "'js_script' is a required parameter")

    _uuid = uuid.uuid1().hex  # a uuid for this request. will be used for output

    static_path = os.path.join(app.root_path, 'static', _uuid)
    os.makedirs(static_path)

    script_path = os.path.join(static_path, "js_script.js")

    script_file = open(script_path, 'w')
    script_file.write(js_script)
    script_file.close()
    args = [
        'casperjs',
        '%s/js_script.js' % static_path
    ]
    print args
    try:
        subprocess.check_call(args, cwd=static_path)
    except subprocess.CalledProcessError:
        return jsonify(status='error', message='There was an error calling the casperjs backend.')
    return jsonify(status='success', download_path=url_for('static', filename='%s/' % (_uuid, )))


@app.route('/examples/basic')
def example():
    return render_template('basic.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
