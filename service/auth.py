import jwt
import uuid
from dotenv import load_dotenv 
load_dotenv()
import os

class Auth:
    def __init__(self):
        self.key = os.getenv('KEY_JWT')
        self.correctPassword = os.getenv('CORRECT_PASSWORD')
        pass

    def checkPassword(self, password):
        if password == self.correctPassword:
            return True
        return False
    
    def encodeToken(self, app):
        session = uuid.uuid4()
        return jwt.encode({
            'session': str(session)
        }, app.config['SECRET_KEY'], algorithm='HS256')
    
    def decodeToken(self, token, app):
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
