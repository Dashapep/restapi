import flask
from flask import jsonify

from data import db_session
import parser
from . import db_session
from .users import User
from flask_restful import reqparse, abort, Api, Resource


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(Users).get(users_id)
        return jsonify({'users': users.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'hashed_password', 'modified_date'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(Users).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'hashed_password', 'modified_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = Users(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            modified_date=args['modified_date']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
