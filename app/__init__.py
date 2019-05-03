from flask import Flask
app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = './app/static/docs'
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])
from app import views
