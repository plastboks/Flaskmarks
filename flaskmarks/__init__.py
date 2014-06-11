# @package flaskmarks
#
# @version 0.12
#
# @author Alexander Skjolden
#
# @date 2013-06-06
#


from flask import Flask
app = Flask(__name__)

from flaskmarks import core
from flaskmarks import models
