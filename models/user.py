from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from configuracion.config import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    is_admin = Column(Boolean, default=False)

    @staticmethod
    def get_user():
        return User.query.first()  # Retorna el primer usuario de la base de datos

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)  # Hash de la contraseña
    
    def check_password(self, password):
        return check_password_hash(self.password, password)  # Verifica la contraseña
