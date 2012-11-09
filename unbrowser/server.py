import os
import subprocess
import uuid
import json

from flask import Flask, request, url_for, abort, jsonify, render_template

from api import Casper, Capture

app = Flask(__name__)


def _param(name, default=None):
    return request.form.get(name, default)


@app.route('/webkit/render/', methods=['POST'])
def render():
    url = _param('url')
    frmt = _param('format', 'png')
    casper_options = _param('casper_options', '{}')

    if not url:
        abort(400, "'url' is a required parameter")

    _uuid = uuid.uuid1().hex  # a uuid for this request. will be used for output

    static_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static', _uuid)
    os.makedirs(static_path)

    render_output_path = os.path.join(static_path, "render.%s" % frmt)
    render_script_path = os.path.join(static_path, "render.js")

    c = Casper(json.loads(casper_options))
    c.start(url, action=Capture(render_output_path))
    c.run()

    script_file = open(render_script_path, 'w')
    script_file.write(c.render())
    script_file.close()

    args = [
        'casperjs',
        render_script_path,
    ]

    subprocess.call(args, stderr=subprocess.STDOUT)
    return jsonify(status='success', download_path=url_for('static', filename='%s/render.%s' % (_uuid, frmt, )))


@app.route('/examples/basic')
def example():
    return render_template('basic.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
