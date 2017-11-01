from flask import Flask
from flask import render_template

app = Flask(__name__) # pylint: disable=invalid-name

import bookapp.routes
