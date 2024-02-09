"""
    Цей Flask додаток забезпечує просту систему реєстрації та входу користувачів.Реалізовано роботу з БД

Маршрути:

    '/' (головна): Відображує домашню сторінку. Якщо користувач не увійшов у систему, перенаправляє на сторінку входу.
    '/about': Відображує сторінку "Про сайт". Якщо користувач не увійшов у систему, перенаправляє на сторінку входу.
    '/register': Відображує сторінку реєстрації та обробляє реєстрацію користувача.
    '/login': Відображує сторінку входу та обробляє вхід користувача.
    '/logout': Виходить користувача шляхом очищення сеансу.
Функції:

    generate_id(length=10): Генерує випадковий ідентифікатор користувача заданої довжини.
    get_user_by_id(user_id): Отримує користувача за його ідентифікатором з бази даних.
    check_user_exists(email): Перевіряє, чи існує користувач з вказаною електронною адресою в базі даних.
    check_user_login(email, password): Перевіряє, чи існує комбінація електронної адреси та пароля в базі даних.
"""

from flask import render_template, Flask, request, redirect, url_for, flash, session
from forms import RegistrationForm, LoginForm
from models import db, UsersDB
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db.init_app(app)


@app.route('/')
def home():
    def secure():  # Перевіряємо чи авторизований користувач якщо ні перенаправляжмо на сторінку входу
        if not session.get('user_id'):
            flash('Будь ласка, увійдіть або зареєструйтеся, щоб переглянути цю сторінку', 'danger')
            return redirect('/login')
        user = get_user_by_id(session.get('user_id'))  # отримуємо інформацію про активеого користувача сесії
        return render_template('home.html', title='Home', user=user)

    return secure()


@app.route('/about')
def about():
    def secure():  # Перевіряємо чи авторизований користувач якщо ні перенаправляжмо на сторінку входу
        if not session.get('user_id'):
            flash('Будь ласка, увійдіть або зареєструйтеся, щоб переглянути цю сторінку', 'danger')
            return redirect('/login')
        all_user = UsersDB.query.all()  # отримуємо список всіх користувачів
        return render_template('about.html', title='About', all_user=all_user)

    return secure()


@app.route('/register', methods=['GET', 'POST'])
def register():
    #  Створюємо об'єкт нашої форми реєстрації
    register_form = RegistrationForm(request.form)
    #  Перевіряємо чи правильно заповнені дані
    if request.method == 'POST' and register_form.validate():
        #  Перевіряємо чи є в базіданих такий користувач
        if check_user_exists(register_form.email.data):
            flash('Користувач з таким email вже зареєстрований!', 'danger')
        #  Якщо немає створюємо нового користувача
        else:
            new_user = UsersDB(  # Генеруємо рандомний ід та беремо з форми інші дані користувача
                user_id=generate_id(),
                username=register_form.username.data,
                email=register_form.email.data,
                password=register_form.password.data
            )
            db.session.add(new_user)  # Додаємо користувача до базт даних
            db.session.commit()
            return redirect(url_for('login'))  # Переходимо на сторінку входу

    # Рендеримо сторінку та форму реєстрації
    return render_template('register.html', register_form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        #  Перевіряємо чи логін і пароль користувача є базі даних
        if check_user_login(login_form.email.data, login_form.password.data):
            #  Встановлення сесійних змінних після успішного входу
            session['user_id'] = check_user_login(login_form.email.data, login_form.password.data)
            #  Редіректим користувача на головну сторінку
            return redirect(url_for('home'))
        else:
            flash('Емейл або пароль не вірний.')

    # Рендеримо сторінку входу та форму входу
    return render_template('login.html', login_form=login_form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # Очистка сесії
    session.clear()
    flash('Ви вийшли з системи', 'success')
    return redirect('/login')  # Повернення на сторінку входу


def generate_id(length=10):  # Генеруємо випадковий ID заданої довжини.
    user_id = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return int(user_id)


def get_user_by_id(user_id):  # Оримуємо користувача по його ід
    user = UsersDB.query.filter_by(user_id=user_id).first()
    return user


def check_user_exists(email):  # Перевіряємо, чи існує користувач з таким email.
    user = UsersDB.query.filter_by(email=email).first()
    return user is not None


def check_user_login(email, password):  # Перевіряємо чи є комбінація емайлу і паролю в базі даних та повертаємо ід
    user = UsersDB.query.filter_by(email=email).first()
    if user and user.password == password:
        return user.user_id if user else None
    return False


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
