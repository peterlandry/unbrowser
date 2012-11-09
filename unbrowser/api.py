import json


class Casper(object):
    def __init__(self, options=None):
        defaults = {
            'viewportSize': {'width': 1024, 'height': 768}
        }
        if options is not None:
            defaults.update(options)
        self.js = ["var casper = require('casper').create(%s);" % json.dumps(defaults)]

    def start(self, url, action=None):
        self.js.append("casper.start('%s', function() {" % url)
        if action is not None:
            self.js.extend(action.js())
        self.js.append("});")

    def then(self, action):
        self.js.append("casper.then(function() {")
        self.js.extend(action.js())
        self.js.append("});")

    def run(self):
        self.js.append("casper.run();")

    def render(self):
        return '\n'.join(self.js)


class Capture(object):
    def __init__(self, filename):
        self.filename = filename

    def js(self):
        return ["this.capture('%s');" % self.filename]
