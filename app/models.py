import uuid
import hashlib

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

# db initialised with application in app.py
db = SQLAlchemy()

class Serializable(object):
    'Helper class for serializing SQLAlchemy objects'

    def dict(self):
        cols = self.__table__.columns
        return {c.name: getattr(self, c.name) for c in cols}

    def json(self):
        return jsonify(self.dict())


class User(db.Model, Serializable):
    __tablename__ = 'user'
    user_id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(64), primary_key=True, unique=True)
    nodes = db.relationship('Node', backref='user', lazy=True)
    
    def __init__(self, **kwargs):
        user_id = uuid.uuid1().hex
        super(User, self).__init__(user_id=user_id, **kwargs)


class Node(db.Model, Serializable):
    __tablename__ = 'node'
    node_id = db.Column(db.String(40), primary_key=True)
    parent_id = db.Column(db.String(40))
    user_id = db.Column(db.String(32), db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.String(2048), nullable=False)
    db.ForeignKeyConstraint(['invoice_id', 'ref_num'], ['invoice.invoice_id', 'invoice.ref_num'])
    # meeting = db.Column(db.DateTime, nullable=False)
    # created = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        node_id = sha1hash(kwargs['parent_id'], kwargs['user_id'])
        super(Node, self).__init__(node_id=node_id, **kwargs)


def sha1hash(self, *args):
    'return sha1 hexdigest of joined args'
    return hashlib.sha1(cat(args).encode('utf-8')).hexdigest()

cat = ''.join
