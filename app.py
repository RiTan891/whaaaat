from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Главная страница
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()

    # Добавление новой привычки
    if request.method == 'POST':
        habit_name = request.form['habit']
        if habit_name:
            c.execute('INSERT INTO habits (name) VALUES (?)', (habit_name,))
            conn.commit()
        return redirect('/')

    # Получаем все привычки
    c.execute('SELECT * FROM habits')
    habits = c.fetchall()

    # Получаем сегодняшние выполненные привычки
    today = date.today().isoformat()
    c.execute('SELECT habit_id FROM habit_logs WHERE date = ?', (today,))
    done_ids = [row[0] for row in c.fetchall()]

    conn.close()
    return render_template('index.html', habits=habits, done_ids=done_ids, today=today)

# Отметить привычку выполненной
@app.route('/mark/<int:habit_id>')
def mark(habit_id):
    today = date.today().isoformat()
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    # Проверка: если уже отмечено, не добавлять повтор
    c.execute('SELECT * FROM habit_logs WHERE habit_id = ? AND date = ?', (habit_id, today))
    if not c.fetchone():
        c.execute('INSERT INTO habit_logs (habit_id, date) VALUES (?, ?)', (habit_id, today))
        conn.commit()
    conn.close()
    return redirect('/')

# Удалить привычку
@app.route('/delete/<int:habit_id>')
def delete(habit_id):
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    c.execute('DELETE FROM habit_logs WHERE habit_id = ?', (habit_id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Статистика по привычке
@app.route('/stats/<int:habit_id>')
def stats(habit_id):
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('SELECT name FROM habits WHERE id = ?', (habit_id,))
    habit = c.fetchone()
    if habit:
        name = habit[0]
        c.execute('SELECT date FROM habit_logs WHERE habit_id = ? ORDER BY date DESC', (habit_id,))
        dates = [row[0] for row in c.fetchall()]
        total = len(dates)
        conn.close()
        return render_template('stats.html', name=name, dates=dates, total=total)
    return redirect('/')
