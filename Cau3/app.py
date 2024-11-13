from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Cấu hình kết nối PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname='user_data',
        user='postgres',    # Thay bằng tên người dùng PostgreSQL của bạn
        password='12345',  # Thay bằng mật khẩu PostgreSQL của bạn
        host='localhost'
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM people')
    data_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data_list=data_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        address = request.form['address']
        hometown = request.form['hometown']
        job = request.form['job']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO people (full_name, age, birth_date, gender, address, hometown, job)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (full_name, age, birth_date, gender, address, hometown, job))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('form.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM people WHERE id = %s', (id,))
    person = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        full_name = request.form['full_name']
        age = request.form['age']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        address = request.form['address']
        hometown = request.form['hometown']
        job = request.form['job']

        cur = conn.cursor()
        cur.execute('''
            UPDATE people
            SET full_name = %s, age = %s, birth_date = %s, gender = %s, address = %s, hometown = %s, job = %s
            WHERE id = %s
        ''', (full_name, age, birth_date, gender, address, hometown, job, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', person=person)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM people WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
