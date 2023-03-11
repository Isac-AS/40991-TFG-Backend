from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from src import db, bcrypt
from src.accounts.models import User

accounts_bp = Blueprint("accounts", __name__)
debug = False

# CRUD functionality
@accounts_bp.route("/accounts/get_users", methods=["GET"])
def get_users():
    """Function used to fetch all users from the database"""
    user_objects = User.query.all()
    dictionaries = [user.as_dict() for user in user_objects]
    response = jsonify(dictionaries)
    return response

@accounts_bp.route("/accounts/delete", methods=["POST"])
@login_required
def delete_user():
    if not current_user.is_admin:
        response = jsonify({'result': False, 'message': 'No tiene los permisos para eliminar un usario.', 'user': None})
        return response
    
    # Get user id from the response
    user_id = request.json.get('id')
    # Find the user in the database
    user: User = db.session.execute(db.select(User).filter_by(id = user_id)).scalar_one()
    # Delete the user
    db.session.delete(user)
    db.session.commit()

    response = jsonify({'result': True, 'message': f'Usario {user.username} eliminado con éxito.', 'user': None})
    return response

@accounts_bp.route("/accounts/modify", methods=["POST"])
@login_required
def modify_user():
    if not current_user.is_admin:
        response = jsonify({'result': False, 'message': 'No tiene los permisos para modificar un usario.', 'user': None})
        return response
    
    # Get user id from the response
    request_user = request.json.get('user')
    # Find the user in the database
    user: User = db.session.execute(db.select(User).filter_by(id = request_user['id'])).scalar_one()
    # Mail validation
    email_validation = db.session.execute(db.select(User).where(User.email == request_user['email']))
    if len(email_validation.all()) > 0:
        response = jsonify({'result': False, 'message': 'Ya existe un usuario con este correo.', 'user': None})
        return response
    # Update the database selected user fields
    user.username = request_user['username']
    user.password = bcrypt.generate_password_hash(request_user['password']).decode('utf-8')
    user.email = request_user['email']
    user.role = request_user['role']
    user.last_modified_by = "Admin"
    user.updated_at = datetime.now()
    # Commiting apparently save the modified user
    db.session.commit()

    response = jsonify({'result': True, 'message': f'Usario modificado con éxito.', 'user': user.as_dict()})
    return response



# LOGIN related functionality
@accounts_bp.route("/register", methods=["POST"])
def register():
    """
    Function used to register a new user.
    The 4 user inputted fields will be extracted from the response.
    A new user entity will be created and added to the database if 
    there is no other entity with the same e-mail.
    
    :return: Success of the register process.
    :rtype: UserRelatedResponse
    """
    if current_user.is_authenticated:
        response = jsonify({'result': False, 'message': 'Hay un usuario registrado en la sesión.', 'user': None})
        return response
    # User schema creation
    user = User(
        username=request.json.get('username'),
        email=request.json.get('email'),
        role=request.json.get('role'),
        password=request.json.get('password'),
        created_by='Self-registration',
        last_modified_by='Self'
        )

    # Check if mail is in use
    result = db.session.execute(db.select(User).where(User.email == user.email))

    # Debug info
    if debug:
        print(f"Posted user:")
        print(f"Nombre: {request.json.get('username')}")
        print(f"Correo: {request.json.get('email')}")
        print(f"Contraseña: {request.json.get('password')}")
        print(f"Rol: {request.json.get('role')}")
        for user_obj in result.scalars():
            print(f"Encontrado: {user_obj.username}, {user_obj.id}")
        print(f"Result.all() length: {len(result.all())}")

    if len(result.all()) > 0:
        response = jsonify({'result': False, 'message': 'Correo electrónico ya en uso.', 'user': None})
        return response
    
    db.session.add(user)
    db.session.commit()
    login_user(user)

    response = jsonify({'result': True, 'message': 'Éxito en el registro de usuario.', 'user': user.as_dict()})
    return response


@accounts_bp.route("/login", methods=["POST"])
def login():
    """
    Function to log in an existing user. Will check wheter there is a user already authenticated and 
    whether the email and password are correct.
    
    :return: Success of the login process
    :rtype: UserRelatedResponse
    """
    if current_user.is_authenticated:
        response = jsonify({'result': False, 'message': 'Hay un usuario registrado en la sesión.', 'user': None})
        return response
    
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Look for the email
    user: User = db.session.execute(db.select(User).filter_by(email = email)).scalar_one()

    if debug:
        print(f"Attempt:\nEmail: {email}\nPassword: {password}")
        print(f"DB object:\n{user.as_dict()}")
        print(f"Check password hash: {bcrypt.check_password_hash(user.password, password)}")
    
    if bcrypt.check_password_hash(user.password, password):
        login_user(user)
        response = jsonify({'result': True, 'message': 'Éxito en el inicio de sesión.', 'user': user.as_dict()})
        return response
    response = jsonify({'result': False, 'message': 'Error en el inicio de sesión.', 'user': None})
    return response


@accounts_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    """Function to log the current user out. Will send a cookie back sayin that it expired de moment this 
    quantum fluctuation of the universe was created, the big bang, also known as 01/01/1970 00:00:00 GMT

    :return: Success of the process
    :rtype: UserRelatedResponse
    """
    logout_user()
    response = jsonify({'result': True, 'message': 'Sesión cerrada con éxito.', 'user': None})
    return response


@accounts_bp.route("/accounts/current_user_data", methods=["GET"])
def user_data():
    """Fetches current user data.

    :return: Will return the status of the request and user data
    :rtype: UserRelatedResponse
    """
    if current_user.is_authenticated:
        response = jsonify({'result': True, 'message': 'Usuario autenticado con los siguientes datos.', 'user': current_user.as_dict()})
        return response
    response = jsonify({'result': False, 'message': 'No hay ningún usuario autenticado.', 'user': None})
    return response


@accounts_bp.route("/accounts/getsession", methods=["GET"])
def check_session():
    """Returns simple UserRelatedResponse with no data, just True or False whether there is a user logged in or not

    :return: Returns whether there is a user authenticated
    :rtype: UserRelatedResponse
    """
    if current_user.is_authenticated:
        response = jsonify({'result': True, 'message': 'Hay un usuario autenticado.', 'user': None})
        return response
    response = jsonify({'result': False, 'message': 'No hay ningún usuario autenticado.', 'user': None})
    return response

def print_logged_in_user():
    if debug and current_user.is_authenticated:
        print("\nCurrent Logged in user:")
        print(f"Username: {current_user.username}")
        print(f"Is authenticated: {current_user.is_authenticated}")
        print(f"Is active: {current_user.is_active}")
        print(f"Is anonymous: {current_user.is_anonymous}")
        print(f"Id: {current_user.get_id()}\n")