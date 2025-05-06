from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import create_database, create_table, get_all_topics, add_topic, get_topic_by_id, update_topic, delete_topic, create_user_table, add_user, get_user_by_username

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

create_database()
create_table()
create_user_table()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    topics = get_all_topics()
    return render_template('index.html', topics=topics)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        add_topic(title, description)
        return redirect(url_for('index'))
    return render_template('add_topic.html')

@app.route('/update/<int:topic_id>', methods=['GET', 'POST'])
def update(topic_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    topic = get_topic_by_id(topic_id)
    if request.method == 'POST':
        new_title = request.form['title']
        new_description = request.form['description']
        update_topic(topic_id, new_title, new_description)
        return redirect(url_for('index'))
    return render_template('update_topic.html', topic=topic)

@app.route('/delete/<int:topic_id>')
def delete(topic_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    delete_topic(topic_id)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = get_user_by_username(username)
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('signup'))
        add_user(username, password)
        flash('Account created successfully. Please login.')
        return redirect(url_for('login'))
    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
