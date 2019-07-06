from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from gymcoin.blockchain import *
from textwrap import dedent
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Instantiate our Node
app = Flask(__name__);

app.config['SECRET_KEY'] = 'Moe Lester wants to talk to you for a Titty Attack';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False;
db = SQLAlchemy(app);
bcrypt = Bcrypt(app);
loginManager = LoginManager(app);
loginManager.login_view = 'login';
loginManager.login_message_category = 'info';
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '');

# Instantiate the Blockchain
blockchainObj = Blockchain();
#print(type(blockchain));

from gymcoin import routes;