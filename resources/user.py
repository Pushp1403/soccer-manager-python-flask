from flask_restful import Resource, reqparse, fields, marshal_with
from services import user_service
from config.errors import UserAlreadyExistsException
from auth import jwt_required, get_jwt_identity
from common.utils import is_valid_email

request_parser = reqparse.RequestParser()
request_parser.add_argument("username", help="username is a mandatory field.", required=True)
request_parser.add_argument("password", help="Password is a mandatory field", required=True)

resource_fields = {
    "username": fields.String
}


class User(Resource):

    @marshal_with(resource_fields)
    def post(self):
        """
        Update user details
        :return:
        """
        args = request_parser.parse_args()
        is_valid_email(args.username)
        if user_service.check_if_user_exists(args.username):
            raise UserAlreadyExistsException(payload=args)
        return user_service.create_user(args.username, args.password)

    @jwt_required
    def get(self):
        """Get user data by username"""
        username = get_jwt_identity()
        return user_service.get_user_data_by_username(username)
