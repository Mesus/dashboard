from flask import Flask
from models import *
from views.produce import produce_br
from app.view import profile
from views.sell import sell
from views.loss import loss
from views.weather import weather_br

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(profile)
app.register_blueprint(produce_br)
app.register_blueprint(sell)
app.register_blueprint(weather_br)
app.register_blueprint(loss)