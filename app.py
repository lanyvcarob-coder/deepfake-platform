from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import bcrypt
import os
from deepfake import analyze_file
from reports import generate_report

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.LargeBinary)
    role = db.Column(db.String(20))

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
    user = User(email=data['email'], password=hashed, role="user")
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode(), user.password):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token})
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    user_id = get_jwt_identity()
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    new_file = File(filename=file.filename, user_id=user_id)
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"msg": "File uploaded"})

@app.route("/analyze/<filename>", methods=["GET"])
@jwt_required()
def analyze(filename):
    result = analyze_file(filename)
    return jsonify(result)

@app.route("/report/<filename>", methods=["GET"])
@jwt_required()
def report(filename):
    analysis = analyze_file(filename)
    report = generate_report(filename, analysis)
    return jsonify(report)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
