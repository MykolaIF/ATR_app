from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from user_dashboard import user_bp
from admin_dashboard import admin_bp

app = Flask(__name__)
app.secret_key = 'my1very2secret3key#'  # Змініть на реальний секретний ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Шлях до бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація SQLAlchemy
db = SQLAlchemy(app)

# Ініціалізація Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Модель користувача
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)


# Функція для завантаження користувача
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Реєстрація Blueprint для user_dashboard
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')


# Головна сторінка
@app.route('/')
def home():
    return redirect(url_for('login'))


# Сторінка авторизації
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            # flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Невірний логін або пароль', 'error')

    return render_template('login.html')


# Сторінка dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard.admin_dashboard'))
    elif current_user.role == 'user':
        return redirect(url_for('user_dashboard.user_dashboard'))
    else:
        return redirect(url_for('login'))


# Вихід
@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('Ви вийшли з системи', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Створення бази даних (якщо вона ще не існує)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
