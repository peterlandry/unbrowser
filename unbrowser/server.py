import os
import subprocess
import uuid
import json

from flask import Flask, redirect, request, url_for, abort, jsonify,render_template
app = Flask(__name__)

def _param(name, default=None):
    return request.form.get(name, default)

@app.route('/webkit/rasterize/', methods=['POST'])
def rasterize():
    url = _param('url')
    width = int(_param('width', 800))
    height = int(_param('height', 600))
    plugins = _param('plugins','no').lower() == 'yes'
    render_delay = int(_param('render_delay', 1000))
    frmt = _param('format', 'png')
    
    if not url:
        abort(400, "'url' is a required parameter")
    
    _uuid = uuid.uuid1().hex # a uuid for this request. will be used for output

    local_output = os.path.join(
        os.path.dirname(os.path.realpath( __file__ )), 'static', 
        "%s.%s" % (_uuid, frmt)
    )
    
    args = [
        'xvfb-run',
        '--server-args=-screen 0, %dx%dx24' % (width+100, height+100),
        'phantomjs',
        '--disk-cache=no',
        'rasterize.js',
        url,
        local_output,
        str(width),
        str(height),
        str(render_delay)
    ]

    subprocess.call(args, stderr=subprocess.STDOUT)
    return jsonify(status='success', download_path=url_for('static', filename='%s.%s' % (_uuid, frmt)))


@app.route('/examples/basic')
def example():
    return render_template('basic.html')






if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

