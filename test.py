from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from gymcoin.blockchain import *
from textwrap import dedent
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

blockchain = Blockchain();

print(type(blockchain.generateKeys()));