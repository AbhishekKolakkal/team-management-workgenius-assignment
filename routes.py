from flask import Blueprint, jsonify, request
from .models import db, Team, User
from .schemas import TeamSchema, UserSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .controllers import fetch_users, fetch_teams, create_team, create_user, edit_team, delete_team, add_user_to_team, remove_user_from_team


ma = Blueprint('managementapp', __name__)


ma.route('/users', methods=['GET'])(fetch_users)
ma.route('/teams', methods=['GET'])(fetch_teams)
ma.route('/teams', methods=['POST'])(create_team)
ma.route('/users', methods=['POST'])(create_user)
ma.route('/teams/<team_id>', methods=['PUT'])(edit_team)
ma.route('/teams/<team_id>', methods=['DELETE'])(delete_team)
ma.route('/teams/<team_id>/users', methods=['POST'])(add_user_to_team)
ma.route('/teams/<team_id>/users', methods=['DELETE'])(remove_user_from_team)

