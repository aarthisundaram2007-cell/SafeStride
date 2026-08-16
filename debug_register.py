from app import app, init_db, get_db
import os

print('cwd=', os.getcwd())
print('db_exists_before=', os.path.exists('database.db'))
init_db()
print('db_exists_after=', os.path.exists('database.db'))

client = app.test_client()
response = client.post(
    '/register',
    data={
        'full_name': 'Debug User',
        'email': 'debug@example.com',
        'phone': '9999999999',
        'password': '123456',
        'confirm_password': '123456'
    },
    follow_redirects=True
)
print('status=', response.status_code)
print('final_path=', response.request.path)

conn = get_db()
count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
print('user_count=', count)
user = conn.execute('SELECT full_name, email FROM users WHERE email=?', ('debug@example.com',)).fetchone()
print('user_row=', tuple(user) if user else None)
conn.close()
