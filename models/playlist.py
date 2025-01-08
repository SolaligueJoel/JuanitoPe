# models/playlist.py
from config import db

class PlayList(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    selected = db.Column(db.Boolean, default=False)