# import necesarry module and libreries
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
# creating RESTful APIs with Flask-RESTful, and
# managing JSON Web Tokens (JWT) with Flask-JWT-Extended.
from flask_jwt_extended import create_access_token,jwt_required,JWTManager,get_jwt_identity

app = Flask(__name__)

app.config['SECRET_KEY'] ='SUPER-SECRET-KEY'
# the secreate key is used for session security 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# sql alcheny is used for database
db=SQLAlchemy(app)
api=Api(app)
# This line creates a Flask-RESTful API instance, 
# which allows you to define RESTful resources easily.
jwt = JWTManager(app)
# This line creates a Flask-JWT-Extended instance, which is
#  used for managing JSON Web Tokens in the application.

# defin model for database
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(200),nullable=False)

with app.app_context():
  db.create_all()

# creating a resource for user registration::
class UserRegistration(Resource):
    def post(self):
        # extracting data from the request
        data = request.get_json()
        username=data['username']
        password=data['password']
        
        # validate the input
        if not username or not password:
            return{'message':'missing username or password'},400
        # checking if a user already exist or taken
        if User.query.filter_by(username=username).first():
            return {'message':'username already taken'},400
        # create a new user and add it to the database
        new_user = User (username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return{'message':'user created successfully'},200


# creating user resource for user login:
class Userlogin(Resource):
    def post(self):
        # extracting data from request
        data=request.get_json()
        username=data['username']
        password=data['password']
        # checking if user name is avaliablew anc password is  correcr
        user=User.query.filter_by(username=username).first()
        if user and user.password == password:
            # then generate a token for user it generate and access the token using
            # flask_flask jwt extend
            access_token=create_access_token(identity=user.id)
            return{"access_token":access_token},200
        return {'message':'invalidcredentials'},401


# define a protected resource that requres jwt authentication
class protectedResource(Resource):
    @jwt_required()
    def get(self):
        # Retrieve the current user's identity from the JWT
        current_user_id= get_jwt_identity()
        return {"message":f"hello user{current_user_id},you acces the protected resource"},200

# adding resources to api 
api.add_resource(UserRegistration,'/register')
api.add_resource(Userlogin,'/login')
# api.add_resource(protectedResource, '/protected')

if __name__ =='__main__':
    app.run(debug=True)