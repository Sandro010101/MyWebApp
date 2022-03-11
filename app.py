import psycopg2
from flask import Flask, render_template, request

app = Flask(__name__)

conn = psycopg2.connect(database=" service_db",
                        user="postgres",
                        password="1488",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if len(username) == 0:
        return render_template('error.html', error="Username пуст")
    elif len(password) == 0:
        return render_template('error.html', error="Password пуст")

    cursor.execute("SELECT * FROM public.users WHERE login=%s AND password=%s", (str(username), str(password)))

    records = list(cursor.fetchall())  # [(1, 'Username', 'login', 'password')]

    if len(records) == 0:
        return render_template('error.html', error="User not found")

    return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])


if __name__ == '__main__':
    app.run()
