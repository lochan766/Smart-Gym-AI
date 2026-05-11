from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Progress
from ai_engine import generate_plan, generate_workout, generate_diet
from chatbot import chatbot_response

import pymysql, os
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smart_gym'
db.init_app(app)
CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# ---------- FRONTEND ----------
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/dashboard')
@login_required
def dash():
    return send_from_directory('../frontend', 'dashboard.html')

@app.route('/css/<path:p>')
def css(p):
    return send_from_directory('../frontend/css', p)

@app.route('/js/<path:p>')
def js(p):
    return send_from_directory('../frontend/js', p)


# ---------- AUTH ----------
@app.route('/register', methods=['POST'])
def register():
    d = request.json
    u = User(username=d['username'], password=generate_password_hash(d['password']))
    db.session.add(u)
    db.session.commit()
    return jsonify({"msg":"registered"})

@app.route('/login', methods=['POST'])
def login():
    d = request.json
    u = User.query.filter_by(username=d['username']).first()

    if u and check_password_hash(u.password, d['password']):
        login_user(u)
        return jsonify({"msg":"ok"})

    return jsonify({"msg":"fail"})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"msg":"out"})

@app.route('/me')
def me():
    if current_user.is_authenticated:
        return jsonify({"id":current_user.id,"name":current_user.username})
    return jsonify({"id":None})


# ---------- AI ----------
@app.route('/ai', methods=['POST'])
@login_required
def ai():
    return jsonify(generate_plan(request.json))


@app.route('/api/workout', methods=['POST'])
@login_required
def workout():
    data = request.json
    plan = generate_workout(data['goal'], data.get('level', 'beginner'))
    return jsonify({"plan": plan})


@app.route('/api/diet', methods=['POST'])
@login_required
def diet():
    data = request.json
    diet = generate_diet(data['weight'], data['goal'])
    return jsonify({"diet": diet})


@app.route('/api/bmi', methods=['POST'])
@login_required
def bmi():
    data = request.json
    bmi = float(data['weight']) / (float(data['height']) ** 2)
    return jsonify({"bmi": round(bmi, 2)})


@app.route('/api/add-calories', methods=['POST'])
@login_required
def add_calories():
    data = request.json

    new = Progress(
        user_id=current_user.id,
        weight=0,
        calories=data['calories']
    )

    db.session.add(new)
    db.session.commit()

    return jsonify({"msg": "saved"})


@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    return jsonify({"reply": chatbot_response(request.json['message'])})


# ---------- RUN ----------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)