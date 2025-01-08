from flask import Flask, render_template, redirect, url_for, request, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_babel import Babel
from flask_admin.contrib.sqla import ModelView
from models.user import User
from models.playlist import PlayList
from models.form import LoginForm
from config import db


# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_view"
login_manager.session_protection = "strong"
babel = Babel(app)

Bootstrap(app)


@app.route('/login_view', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()

    if form.validate_on_submit():
        # Busca al usuario por su nombre de usuario
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):  # Comparar el hash de la contraseña
            login_user(user, remember=form.remember.data)
            flash('Login exitoso.', 'success')
            return redirect(url_for('admin_panel.index')) 
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html', form=form) # Renderizamos el formulario de login

# Cargar usuario en sesión
@login_manager.user_loader
def load_user(user_id):
    if int(user_id) == 1:  # Solo el usuario admin tiene ID 1
        return User.get_user()
    return None

# Vista personalizada para el índice del admin
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(MyAdminIndexView, self).index()

# Vista personalizada de administración de PlayList
class PlayListAdminView(ModelView):
    def is_accessible(self):
        # Aseguramos que solo el admin logueado pueda acceder
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        # Redirige a la página de login si el usuario no tiene acceso
        return redirect(url_for('login_view'))
# Inicializar Admin con un nombre de blueprint único
admin = Admin(app, name='JuanitoPeApp', index_view=MyAdminIndexView(name='Panel de Control', endpoint='admin_panel'))
admin.add_view(PlayListAdminView(PlayList, db.session))

# Rutas públicas
@app.route('/')
def user():
    songs = PlayList.query.all()
    return render_template('user.html', songs=songs)

@app.route('/select/<int:song_id>', methods=['POST'])
def select_song(song_id):
    song = PlayList.query.get(song_id)
    if song:
        song.selected = True
        db.session.commit()
    return redirect(url_for('user'))

@app.route('/deselect/<int:song_id>', methods=['POST'])
def deselect_song(song_id):
    song = PlayList.query.get(song_id)
    if song:
        song.selected = False
        db.session.commit()
    return redirect(url_for('user'))

# Inicializar la base de datos y datos de prueba
with app.app_context():
    db.create_all()
    # Verificar si ya existe un usuario admin
    admin = User.query.filter_by(username='admin').first()

    if not admin:
        # Si no existe, crear el usuario admin
        admin = User(username='admin')
        admin.set_password('admin_password')
        admin.is_admin = True
        
        # Guardar el usuario en la base de datos
        db.session.add(admin)
        db.session.commit()
        print('Usuario admin creado con éxito!')
    else:
        print('El usuario admin ya existe. No se creará de nuevo.')

    if not PlayList.query.first():
        playlists = [
            PlayList(name="Song 1", author="Author 1"),
            PlayList(name="Song 2", author="Author 2"),
            PlayList(name="Song 3", author="Author 3"),
        ]
        db.session.add_all(playlists)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
