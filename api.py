from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Database Model
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"

# Request Parser
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=False, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=False, help="Email cannot be blank")

# Serialization Fields
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}

# Resources
class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        """Retrieve all users."""
        users = UserModel.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        """Create a new user."""
        args = user_args.parse_args()
        if UserModel.query.filter_by(email=args['email']).first():
            abort(409, message="Email already exists")
        user = UserModel(name=args['name'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

class User(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        """Retrieve a single user by ID."""
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(user_fields)
    def patch(self, id):
        """Partially update a user by ID."""
        args = user_args.parse_args()
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        
        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
        db.session.commit()
        return user

    def delete(self, id):
        """Delete a user by ID."""
        user = UserModel.query.get(id)
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204

# Resource Routes
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

# Home Route
@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database is initialized
    app.run(debug=True)
