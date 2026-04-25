from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB = 'blog.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS post (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')

@app.route('/')
def post_list():
    with get_db() as conn:
        posts = conn.execute('SELECT * FROM post ORDER BY created_at DESC').fetchall()
    return render_template('post_list.html', posts=posts)

@app.route('/post/<int:id>')
def post_detail(id):
    with get_db() as conn:
        post = conn.execute('SELECT * FROM post WHERE id = ?', (id,)).fetchone()
    if post is None:
        return '404 Not Found', 404
    return render_template('post_detail.html', post=post)

@app.route('/write', methods=['GET', 'POST'])
def write_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now().strftime('%b %d, %Y')
        with get_db() as conn:
            conn.execute(
                'INSERT INTO post (title, content, created_at) VALUES (?, ?, ?)',
                (title, content, created_at)
            )
        return redirect(url_for('post_list'))
    return render_template('write_post.html')

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    with get_db() as conn:
        post = conn.execute('SELECT * FROM post WHERE id = ?', (id,)).fetchone()
    if post is None:
        return '404 Not Found', 404
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with get_db() as conn:
            conn.execute(
                'UPDATE post SET title = ?, content = ? WHERE id = ?',
                (title, content, id)
            )
        return redirect(url_for('post_detail', id=id))
    return render_template('write_post.html', post=post)

@app.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    with get_db() as conn:
        conn.execute('DELETE FROM post WHERE id = ?', (id,))
    return redirect(url_for('post_list'))

init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
