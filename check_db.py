import sqlite3
from werkzeug.security import check_password_hash

DATABASE = "budget.db"

# Подключаемся к базе данных
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# 1. Ищем пользователя test_user
cursor.execute('SELECT * FROM user WHERE username = ?', ('test_user',))
user_from_db = cursor.fetchone()

if user_from_db:
    print(f"[УСПЕХ] Найден пользователь: {user_from_db['username']}")
    print(f"Его хэш пароля в БД: {user_from_db['password_hash']}")
    print("---")
    
    # 2. Проверяем, совпадает ли хэш от 'password' с тем, что в базе
    is_correct = check_password_hash(user_from_db['password_hash'], 'password')
    print(f"Пароль 'password' правильный?", is_correct)
    
    # 3. Если нет, пробуем другие возможные варианты
    if not is_correct:
        print("Пароль 'password' не подошел. Проверяем другие варианты...")
        for possible_pass in ['test_password', '123456', 'qwerty']:
            check_result = check_password_hash(user_from_db['password_hash'], possible_pass)
            print(f"Пароль '{possible_pass}' правильный?", check_result)
else:
    print("[ОШИБКА] Пользователь test_user не найден в БД!")

# 4. Дополнительно: посмотрим, есть ли вообще пользователи и какие
print("\n--- Дополнительная информация ---")
cursor.execute('SELECT id, username FROM user')
all_users = cursor.fetchall()
print(f"Всего пользователей в БД: {len(all_users)}")
for user in all_users:
    print(f"ID: {user['id']}, Username: {user['username']}")

conn.close()