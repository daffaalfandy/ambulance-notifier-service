from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from marshmallow import fields  #serialize python object
from marshmallow_sqlalchemy import ModelSchema  #serialize python object
import os
import bcrypt

load_dotenv('.env')

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# User Model
class User(db.Model):
    __tablename__ = "users"
    id_user = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
# Ambulance Model
class Ambulance(db.Model):
    __tablename__ = "ambulances"
    id_ambulance = db.Column(db.Integer, primary_key=True)
    ambulance_type = db.Column(db.String(255))
    ambulance_status = db.Column(db.Integer)
    ambulance_origin = db.Column(db.String())
    license_plate = db.Column(db.String(100))

    def __init__(self, ambulance_type, ambulance_status, ambulance_origin, license_plate):
        self.ambulance_type = ambulance_type
        self.ambulance_origin = ambulance_origin
        self.ambulance_status = ambulance_status
        self.license_plate = license_plate

# User Schema
class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    
    id_user = fields.Number(dump_only=True)
    fullname = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
# Ambulance Schema
class AmbulanceSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Ambulance
        sqla_session = db.session
    id_ambulance = fields.Number(dump_only=True)
    ambulance_type = fields.String(required=True)
    ambulance_status = fields.Integer(required=True)
    ambulance_origin = fields.String(required=True)
    license_plate = fields.String(required=True)

# User endpoint
@app.route('/api/user', methods=['POST'])
def store_user():
    data = request.get_json()

    pw_hash = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
    data['password'] = pw_hash

    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    result['password'] = None
    return make_response(jsonify({'success': 1, 'result': result}), 200)

@app.route('/api/user/login', methods=['POST'])
def login_user():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return make_response(jsonify({'success': 0, 'msg': 'Missing email!'}), 400)
    if not password:
        return make_response(jsonify({'success': 0, 'msg': 'Missing password!'}), 400)

    user = User.query.filter_by(email=email).first()    
    
    if not user:
        return make_response(jsonify({'success': 0, 'msg': 'Email not found!'}), 404)

    if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        return make_response(jsonify({
            'success': 1,
            'msg': 'Login Successful',
            'user': {
                'email': user.email,
                'fullname': user.fullname
            }
        }), 200)
    else:
        return make_response(jsonify({'success': 0, 'msg': 'Wrong password!'}), 400)

    return make_response(jsonify({'email': email, 'password': password}))

# Run server
if __name__ == "__main__":
    app.run(debug=True)