from flask import Flask
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
metrics = PrometheusMetrics(app)

from models import *

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Database initialization failed:", e)

@app.get("/health")
def health():
    return {"status": "healthy"}, 200

@app.get("/ready")
def ready():
    try:
        # Execute a lightweight PostgreSQL connectivity check
        db.session.execute(db.text('SELECT 1'))
        return {"status": "ready"}, 200
    except Exception:
        return {"status": "not ready"}, 503



@app.route('/', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text']
    post = Post(text)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
