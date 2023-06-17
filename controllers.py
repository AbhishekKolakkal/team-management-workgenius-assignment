from flask import jsonify, request
from .models import User, Team
from .schemas import UserSchema, TeamSchema
from .database import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

def fetch_users():
    print("skndjbdbd")
    try:
        users = User.query.all()
        result = [{'id': user.id, 'name': user.name} for user in users]
        print(result)
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({'message': "No user Found"})


def fetch_teams():
    user_id = request.args.get('user_id')
    teams = Team.query.filter_by(user_id=user_id).all()
    result = [{'id': team.id, 'name': team.name, 'description': team.description} for team in teams]
    return jsonify(result)


def create_team():
    data = request.get_json()
    print(data)
    team_data = TeamSchema(**data)
    try:
        team = Team(name=team_data.name, description=team_data.description, user_id=int(team_data.user_id))
        db.session.add(team)
        db.session.commit()
        return jsonify({'message': 'Team created successfully'})
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return jsonify({'error': 'Team name already exists'}), 400


def create_user():
    data = request.get_json()
    print(data)
    user_data = UserSchema(**data)
    try:
        user = User(name=user_data.name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User name already exists'}), 400


# this should only be done id the user id is passed and only that should get updated or else should give response that "team does not exist in your base" after this only name is only passed only name should get updated same goes for description 
def edit_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404

    data = request.get_json()
    user_id = request.args.get('user_id')

    if user_id is None or int(user_id) != team.user_id:
        return jsonify({'error': 'Team does not exist in your base'})

    if 'name' in data:
        team.name = data['name']

    if 'description' in data:
        team.description = data['description']

    db.session.commit()

    return jsonify({'message': 'Team updated successfully'})


def delete_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404

    user_id = request.args.get('user_id')


    if user_id is None or int(user_id) != team.user_id:
        return jsonify({'error': 'Team does not exist in your base'})


    db.session.delete(team)
    db.session.commit()

    return jsonify({'message': 'Team deleted successfully'})


def add_user_to_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404

    data = request.get_json()
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    team.user_id = user_id
    db.session.commit()

    return jsonify({'message': 'User added to team successfully'})


def remove_user_from_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        return jsonify({'error': 'Team not found'}), 404

    team.user_id = None
    db.session.commit()

    return jsonify({'message': 'User removed from team successfully'})
