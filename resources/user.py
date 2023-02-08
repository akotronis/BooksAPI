from sqlite3 import IntegrityError
from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema


blp_v1 = Blueprint("Users-v1", __name__)


@blp_v1.route("/users/register")
class UserRegister(MethodView):
    @blp_v1.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
                username=user_data["username"],
                password=pbkdf2_sha256.hash(user_data["password"])
            )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A user with this username already exists")
        except:
            db.session.rollback()
            abort(500, message="Could not register user")
        return {"message": "User created succesfully"}, 201


@blp_v1.route("/users/login")
class UserLogin(MethodView):
    @blp_v1.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {
                "access_token": access_token,
            }
        abort(401, message="Invalid credentials")


@blp_v1.route("/users/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        print(BLOCKLIST)
        print(get_jwt())
        return {"message": "Successfully logged out."}


@blp_v1.route("/users/<int:user_id>")
class User(MethodView):

    @jwt_required()
    @blp_v1.response(200, UserSchema)
    def get(self, user_id):
        if get_jwt()["sub"] != user_id:
            abort(401, message="User missmatched. Could not get user")
        user = UserModel.query.get_or_404(user_id)
        # If we want to make sure we don't send password to Schema in the first place:
        # user = UserModel.query.with_entities(UserModel.username).filter(UserModel.id==user_id).first()
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        if get_jwt()["sub"] != user_id:
            abort(401, message="User missmatched. Could not delete user")
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            abort(500, message="Could not delete user")
        return {"message": "User deleted succesfully"}, 200