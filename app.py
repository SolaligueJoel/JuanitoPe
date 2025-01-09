from flask import Flask, render_template, redirect, url_for, flash, request
from flask_admin import Admin, AdminIndexView, expose
from flask_login import LoginManager, login_user, login_required, current_user
from werkzeug.security import check_password_hash
from flask_bootstrap5 import Bootstrap
from flask_babel import Babel
from flask_admin.contrib.sqla import ModelView
import os
from models.user import User
from models.playlist import PlayList, Genero
from models.form import LoginForm
from configuracion.config import db, Config


# Configuración de la aplicación
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path ,'configuracion','config.ini')

db_config = Config('db', config_path_name)
server_config = Config('server', config_path_name)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"

# Inicializar extensiones
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_view"
login_manager.session_protection = "strong"
babel = Babel(app)

Bootstrap(app)

# Lista de canciones seleccionadas
selected_songs = []


@app.route('/login_view', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel.index'))

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
        selected_songs = db.session.query(PlayList).filter_by(selected=True)

        return self.render('admin/index.html', songs=selected_songs)

# Vista personalizada de administración de PlayList
class PlayListAdminView(ModelView):
    def is_accessible(self):
        # Aseguramos que solo el admin logueado pueda acceder
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirige a la página de login si el usuario no tiene acceso
        return redirect(url_for('login_view'))

class GeneroView(ModelView):
    form_columns = ["name"]

# Inicializar Admin con un nombre de blueprint único
admin = Admin(app, name='JuanitoPeApp', index_view=MyAdminIndexView(name='Panel de Control', endpoint='admin_panel'))
admin.add_view(PlayListAdminView(PlayList, db.session))
admin.add_view(GeneroView(Genero,db.session))

@app.route('/<int:page_num>')
def user(page_num):
    genero_id = request.args.get('genero')
    
    # Consulta básica
    query = PlayList.query

    # Aplicar filtro si se seleccionó un género
    if genero_id:
        query = query.filter_by(genero_id=genero_id)
    
    # Paginación
    songs = query.paginate(per_page=20, page=page_num, error_out=True)

    # Obtener todos los géneros para el filtro
    generos = Genero.query.all()

    return render_template('user.html', songs=songs, generos=generos)


@app.route('/select/<int:song_id>', methods=['POST'])
def select_song(song_id):
    song = db.session.query(PlayList).filter_by(id=song_id, selected=False).first()
    print(song)
    if song:
        if(song.selected == False):
            song.selected = True
            db.session.commit()
        song_selected = PlayList.query.paginate()
        song_selected_page = song_selected.page
        print(song_selected_page)
    return redirect(url_for('user', page_num=song_selected_page))

@app.route('/deselect/<int:song_id>', methods=['POST'])
def deselect_song(song_id):
    song = PlayList.query.get(song_id)
    if song:
        if(song.selected == True):
            song.selected = False
            db.session.commit()
        song_selected = PlayList.query.paginate()
        song_selected_page = song_selected.page
    return redirect(url_for('user', page_num=song_selected_page))

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

if __name__ == '__main__':
    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)
