from configuracion.config import db

class PlayList(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    selected = db.Column(db.Boolean, default=False)
    genero_id = db.Column(db.Integer, db.ForeignKey("genero.id"), nullable=False)
    genero = db.relationship("Genero", back_populates="playlist")

    def __str__(self):
        return self.name

class Genero(db.Model):
    __tablename__ = "genero"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    playlist = db.relationship("PlayList", back_populates = "genero")

    def __str__(self):
        return self.name