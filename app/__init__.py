from flask import Flask
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] ='mybook'


mysql = MySQL(app)
app.config['POST_PICS'] = "app\static\post_pics"
app.config['SECRET_KEY'] = "secret key"

app.config.from_object(__name__)
from app import views
