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

# User Schema
class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    
    id_user = fields.Number(dump_only=True)
    fullname = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)

# User endpoint
@app.route('/api/user', methods=['POST'])
def store_user():
    data = request.get_json()

    pw_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    data['password'] = pw_hash

    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    result['password'] = None
    return make_response(jsonify({'success': 1, 'result': result}), 200)

# Run server
if __name__ == "__main__":
    app.run(debug=True)