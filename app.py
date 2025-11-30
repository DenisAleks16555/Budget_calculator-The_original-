from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import sqlite3
from flask import jsonify

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

DATABASE = "budget.db"  # Упростил путь

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['DEBUG'] = DEBUG

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                category TEXT  -- Добавил столбец category
            )
        ''')
        cursor.execute('SELECT COUNT(*) FROM expenses')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO expenses (description, amount, date, category) VALUES (?, ?, ?, ?)",
                           ('Покупка продуктов', 5000, '2025-09-10', 'Еда'))
            cursor.execute("INSERT INTO expenses (description, amount, date, category) VALUES (?, ?, ?, ?)",
                           ('Такси', 1200, '2025-09-10', 'Транспорт'))
        conn.commit()

@app.route('/expenses')
def get_expenses():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    expenses_list = [dict(expense) for expense in expenses]
    return jsonify(expenses_list)

@app.route('/')
def index():
    conn = get_db_connection()
    expenses = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    total = sum([expense['amount'] for expense in expenses])
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=('GET', 'POST'))
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        date = request.form['date']
        category = request.form.get('category', '')  # Добавил обработку category
        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (description, amount, date, category) VALUES (?, ?, ?, ?)',
                     (description, amount, date, category))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

# Сделать сайт удобным для мобильных устройств
# Сделать так, чтобы сайт хорошо выглядел и работал на телефонах и планшетах. Это называется адаптивный дизайн.








# from flask import Flask, render_template, request, redirect, url_for, flash
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import func
# import os
# load_dotenv()

# app = Flask(__name__)

# # Конфигурация: база SQLite в файле budget.db
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(BASE_DIR, 'budget.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# # # ===========================
# # # Модели
# # # ===========================

# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<Category {self.name}>'

# class Transaction(db.Model):
#     __tablename__ = 'transactions'
#     id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float, nullable=False)
#     description = db.Column(db.String(255))
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
#     category = db.relationship('Category', backref=db.backref('transactions', lazy=True))
#     date = db.Column(db.Date, nullable=False, server_default=func.current_date())

#     def __repr__(self):
#         return f'<Transaction {self.amount} {self.description}>'

# # # ===========================
# # # Маршруты
# # # ===========================

# @app.before_first_request
# def create_tables():
#     # Создаём таблицы, если их нет
#     db.create_all()

# @app.route('/')
# def index():
#     # Простейшая страница: вывод баланса по категориям и общая сумма
#     total = db.session.query(func.sum(Transaction.amount)).scalar() or 0.0
#     # сумма по категориям
#     by_category = (
#         db.session.query(Category.name, func.sum(Transaction.amount).label('sum_amt'))
#         .outerjoin(Transaction)
#         .group_by(Category.name)
#         .all()
#     )
#     # Простой список транзакций для вывода
#     transactions = Transaction.query.order_by(Transaction.date.desc()).limit(20).all()

#     return render_template('index.html', total=total, by_category=by_category, transactions=transactions)

# @app.route('/add_category', methods=['POST'])
# def add_category():
#     name = request.form.get('name', '').strip()
#     if not name:
#         flash('Название категории не может быть пустым', 'error')
#         return redirect(url_for('index'))
#     if Category.query.filter_by(name=name).first():
#         flash('Категория с таким именем уже существует', 'error')
#         return redirect(url_for('index'))
#     category = Category(name=name)
#     db.session.add(category)
#     db.session.commit()
#     flash('Категория добавлена', 'success')
#     return redirect(url_for('index'))

# @app.route('/add_transaction', methods=['POST'])
# def add_transaction():
#     try:
#         amount = float(request.form.get('amount', 0))
#     except ValueError:
#         flash('Недопустимое значение суммы', 'error')
#         return redirect(url_for('index'))
#     description = request.form.get('description', '')
#     category_id = request.form.get('category_id')
#     if category_id:
#         category = Category.query.get(category_id)
#         if not category:
#             flash('Указана неверная категория', 'error')
#             return redirect(url_for('index'))
#     else:
#         category = None

#     t = Transaction(amount=amount, description=description, category=category)
#     db.session.add(t)
#     db.session.commit()
#     flash('Транзакция добавлена', 'success')
#     return redirect(url_for('index'))

# @app.route('/delete_transaction/<int:tid>', methods=['POST'])
# def delete_transaction(tid):
#     t = Transaction.query.get_or_404(tid)
#     db.session.delete(t)
#     db.session.commit()
#     flash('Транзакция удалена', 'success')
#     return redirect(url_for('index'))

# # # ===========================
# # # Запуск сервера
# # # ===========================

# if __name__ == '__main__':
#     # Убеждаемся, что директория для БД существует
#     os.makedirs(BASE_DIR, exist_ok=True)
#     app.run(debug=True)




# Последний из вариантов
# from flask import Flask, render_template, request, redirect, url_for, flash
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import func
# import os
# load_dotenv()

# # Конфигурация приложения
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# app = Flask(__name__)
# # Замените на ваш секретный ключ и путь к БД, если нужно
# app.config['SECRET_KEY'] = 'your-secret-key'  # замените на реальный секрет
# # Пример: SQLite база данных в каталоге проекта
# db_path = os.path.join(BASE_DIR, 'sqlite_budget.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # ===========================
# # Модели
# # ===========================

# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True, nullable=False)

#     def __repr__(self):
#         return f'<Category {self.name}>'

# class Transaction(db.Model):
#     __tablename__ = 'transactions'
#     id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float, nullable=False)
#     description = db.Column(db.String(255))
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
#     category = db.relationship('Category', backref=db.backref('transactions', lazy=True))
#     date = db.Column(db.Date, nullable=False, server_default=func.current_date())

#     def __repr__(self):
#         return f'<Transaction {self.amount} {self.description}>'

# # ===========================
# # Маршруты
# # ===========================

# @app.before_first_request
# def create_tables():
#     # Создаём таблицы, если их нет
#     db.create_all()

# @app.route('/')
# def index():
#     # Простейшая страница: вывод баланса по категориям и общая сумма
#     total = db.session.query(func.sum(Transaction.amount)).scalar() or 0.0
#     # сумма по категориям
#     by_category = (
#         db.session.query(Category.name, func.sum(Transaction.amount).label('sum_amt'))
#         .outerjoin(Transaction)
#         .group_by(Category.name)
#         .all()
#     )
#     # Простой список транзакций для вывода
#     transactions = Transaction.query.order_by(Transaction.date.desc()).limit(20).all()

#     return render_template('index.html', total=total, by_category=by_category, transactions=transactions)

# @app.route('/add_category', methods=['POST'])
# def add_category():
#     name = request.form.get('name', '').strip()
#     if not name:
#         flash('Название категории не может быть пустым', 'error')
#         return redirect(url_for('index'))
#     if Category.query.filter_by(name=name).first():
#         flash('Категория с таким именем уже существует', 'error')
#         return redirect(url_for('index'))
#     category = Category(name=name)
#     db.session.add(category)
#     db.session.commit()
#     flash('Категория добавлена', 'success')
#     return redirect(url_for('index'))

# @app.route('/add_transaction', methods=['POST'])
# def add_transaction():
#     try:
#         amount = float(request.form.get('amount', 0))
#     except ValueError:
#         flash('Недопустимое значение суммы', 'error')
#         return redirect(url_for('index'))
#     description = request.form.get('description', '')
#     category_id = request.form.get('category_id')
#     if category_id:
#         category = Category.query.get(category_id)
#         if not category:
#             flash('Указана неверная категория', 'error')
#             return redirect(url_for('index'))
#     else:
#         category = None

#     t = Transaction(amount=amount, description=description, category=category)
#     db.session.add(t)
#     db.session.commit()
#     flash('Транзакция добавлена', 'success')
#     return redirect(url_for('index'))

# @app.route('/delete_transaction/<int:tid>', methods=['POST'])
# def delete_transaction(tid):
#     t = Transaction.query.get_or_404(tid)
#     db.session.delete(t)
#     db.session.commit()
#     flash('Транзакция удалена', 'success')
#     return redirect(url_for('index'))

# # ===========================
# # Запуск сервера
# # ===========================

# if __name__ == '__main__':
#     # Убеждаемся, что директория для БД существует
#     os.makedirs(BASE_DIR, exist_ok=True)
#     app.run(debug=True)












# from flask import Flask, render_template, request, redirect, url_for
# from dotenv import load_dotenv
# import os
# load_dotenv() # читает .env и кладёт значения в окружение

# import sqlite3
# from datetime import datetime
# from flask import jsonify



# load_dotenv() # читает .env и кладёт значения в окружение

# #app = Flask(name)

# #Конфигурация из .env (если переменные не заданы — используются значения по умолчанию)
# SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key'); DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# #Путь к БД (удобно держать файл бюджета в repo, как сейчас)

# app = Flask(__name__)
# DATABASE = 'budget.db'

# DATABASE = os.environ.get('DATABASE_URL', 'budget.db') # можно использовать 'budget.db' напрямую

# app.secret_key = SECRET_KEY; app.config['DEBUG'] = DEBUG

# def get_db_connection():
#     # Если DATABASE содержит путь, можно использовать напрямую
#     conn = sqlite3.connect(DATABASE)
#     conn.row_factory = sqlite3.Row
#     return conn

# # Инициализация базы данных при запуске
# def init_db():
#     with get_db_connection() as conn:
#         cursor = conn.cursor()
#         # Создаем таблицу, если еще не существует
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS expenses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             description TEXT NOT NULL,
#             amount REAL NOT NULL,
#             date TEXT NOT NULL
#         )
#         ''')
#         # Проверка и добавление начальных данных (если их еще нет)
#         cursor.execute('SELECT COUNT(*) FROM expenses')
#         count = cursor.fetchone()[0]
#         if count == 0:
#             cursor.execute("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)",
#                            ('Покупка продуктов', 5000, '2025-09-10'))
#             cursor.execute("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)",
#                            ('Такси', 1200, '2025-09-10'))
#         conn.commit()

# @app.route('/expenses')
# def get_expenses():
#     conn = get_db_connection()
#     expenses = conn.execute('SELECT * FROM expenses').fetchall()
#     conn.close()
#     # преобразуем расходы в список словарей
#     expenses_list = [dict(expense) for expense in expenses]
#     return jsonify(expenses_list)

# @app.route('/')
# def index():
#     conn = get_db_connection()
#     expenses = conn.execute('SELECT * FROM expenses').fetchall()
#     conn.close()
#     # cursor = conn.cursor()
#     # expenses = cursor.execute("SELECT * FROM expenses").fetchall()
#     # total = sum([expense['amount'] for expense in expenses])
#     return render_template('index.html', expenses=expenses) 
# # , total=total)

# @app.route('/add', methods=('GET', 'POST'))
# def add_expense():
#     if request.method == 'POST':
#         description = request.form['description']
#         amount = float(request.form['amount'])
#         date = request.form['date']
#         conn = get_db_connection()
#         # c = conn.cursor()
#         conn.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)',
#                   (description, amount, date))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('index'))
#     return render_template('add_expense.html')

# @app.route('/delete/<int:expense_id>', methods=['POST'])
# def delete_expense(expense_id):
#     conn = get_db_connection()
#     c = conn.cursor()
#     c.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
#     conn.commit()
#     conn.close()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     init_db()
#     app.run(debug=True) # app.run(debug=Debug)

# 
# Сделать сайт удобным для мобильных устройств
# Сделать так, чтобы сайт хорошо выглядел и работал на телефонах и планшетах. Это называется адаптивный дизайн.












# @app.route('/delete/<int:expense_id>', methods=['POST'])
# def delete_expense(expense_id):
#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
#     conn.commit()
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     init_db()  # Инициализируем базу данных при запуске
#     app.run(debug=True)
   
# init_db()

# # Главная страница - список расходов и итог
# @app.route('/')
# def index():
#     conn = sqlite3.connect('budget.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM expenses')
#     expenses = c.fetchall()
#     total = sum([expense[2] for expense in expenses])  # сумма по полю amount
#     conn.close()
#     return render_template('index.html', expenses=expenses, total=total)

# # Страница для добавления расхода (форма)
# @app.route('/add', methods=['GET', 'POST'])
# def add_expense():
#     if request.method == 'POST':
#         description = request.form['description']
#         amount = float(request.form['amount'])
#         date = request.form['date']
#         conn = sqlite3.connect('budget.db')
#         c = conn.cursor()
#         c.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)',
#                   (description, amount, date))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('index'))
#     return render_template('add_expense.html')

# from flask import redirect, url_for

# @app.route('/delete/<int:expense_id>', methods=['POST'])
# def delete_expense(expense_id):
#     # тут нужно написать код удаления из базы данных
#     # например:
#     # db.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
#     # или, если используете SQLAlchemy:
#     # expense = Expense.query.get(expense_id)
#     # db.session.delete(expense)
#     # db.session.commit()
#     conn = sqlite3.connect('budget.db')
#     c = conn.cursor()
#     c.execute('DELETE FROM expenses WHERE id=?', (expense_id,))
#     conn.commit()
#     conn.close()
#     # После удаления перенаправим обратно на страницу с расходами
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)
