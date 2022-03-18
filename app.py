import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = psycopg2.connect(database=" service_db",
                        user="postgres",
                        password="1488",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM public.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if len(login) == 0:
            return render_template('registration.html', error="login пуст")
        elif len(password) == 0:
            return render_template('registration.html', error="Password пуст")
        cursor.execute(f"SELECT * FROM users WHERE login='{str(login)}'")
        try:
            print(list(cursor.fetchall())[0])

            return render_template('error.html', error="Такой пользователь уже существует")
        except:
            cursor.execute(
                f"INSERT INTO public.users (full_name, login, password) VALUES ('{str(name)}', '{str(login)}', '{str(password)}');")
            conn.commit()
            return redirect('/login/')

    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
