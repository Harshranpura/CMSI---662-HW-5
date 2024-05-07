import jwt 
import sqlite3
from datetime import datetime, timedelta
import passlib 
from passlib.hash import pbkdf2_sha256
from flask import request, g

 # This is the correct import for PyJWT

SECRET_KEY = 'bfg28y7efg238re7r6t32gfo23vfy7237yibdyo238do2v3'

def get_user_with_credentials(email, password):
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT email, name, password FROM users where email=?''',
            (email,))
        row = cur.fetchone()
        if row is None:
            return None
        email, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()

def logged_in():
    token = request.cookies.get('auth_token')
    if not token:
        return False
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        g.user = data['sub']  # Assuming 'sub' is where you store user identifier
        return True
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return False
    except jwt.InvalidTokenError:
        print("Invalid token")
        return False


def create_token(email):
    now = datetime.utcnow()
    payload = {'sub': email, 'iat': now, 'exp': now + timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')  # Correct usage
    return token
