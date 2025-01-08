from flask import Flask, render_template, redirect, url_for, request, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_babel import Babel
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
Bootstrap(app)
babel = Babel(app)

# Modelo de usuario
class User(UserMixin):
    id = 1
    username = "admin"
    password_hash = generate_password_hash("password")

    @staticmethod
    def get_user():
        return User()

@login_manager.user_loader
def load_user(user_id):
    return User.get_user() if user_id == "1" else None

# Modelo de playlist
class PlayList(db.Model):
    __tablename__ = "playlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    selected = db.Column(db.Boolean, default=False)

# Vista personalizada para AdminIndexView
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()

# Agregar administrador con vistas protegidas
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(ModelView(PlayList, db.session))

# Rutas de la aplicación
@app.route("/")
def user():
    songs = PlayList.query.all()
    return render_template("user.html", songs=songs)

@app.route("/select/<int:song_id>", methods=["POST"])
def select_song(song_id):
    song = PlayList.query.get(song_id)
    if song:
        song.selected = True
        db.session.commit()
    return redirect(url_for("user"))

@app.route("/deselect/<int:song_id>", methods=["POST"])
def deselect_song(song_id):
    song = PlayList.query.get(song_id)
    if song:
        song.selected = False
        db.session.commit()
    return redirect(url_for("user"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.get_user()
        if user.username == username and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("admin.index"))
        else:
            flash("Credenciales inválidas", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Inicializar la base de datos
with app.app_context():
    db.create_all()
    if not PlayList.query.first():
        playlists = [
            PlayList(name="Song 1", author="Author 1"),
            PlayList(name="Song 2", author="Author 2"),
            PlayList(name="Song 3", author="Author 3"),
        ]
        db.session.add_all(playlists)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
