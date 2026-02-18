import pickle
import hashlib
import os
import hmac
from dataclasses import dataclass

from server.server_constants import ServerConstants



@dataclass
class User:
    username: str
    hashed_password: str
    email: str
    salt: str

class DataBase:
    USER_DATA = {}

    @staticmethod
    def load():
        try:
            with open(ServerConstants.DB,"rb") as data:
                DataBase.USER_DATA = pickle.load(data)
        except Exception as e:
            print("Failed to load USER_DATA")

    @staticmethod
    def save():
        with open(ServerConstants.DB,"wb") as data:
            pickle.dump(DataBase.USER_DATA, data)

    @staticmethod
    def GetUserEmail(username):
        return DataBase.USER_DATA[username].email

    @staticmethod
    def SaveUser(username, email, password):
        salt, hashed_password = DataBase.hash_password(password)
        DataBase.USER_DATA[username] = User(username, hashed_password, email, salt)

        DataBase.save()
        
    @staticmethod
    def hash_password(password):
        salt = os.urandom(16)

        combined = password.encode("utf-8") + salt + ServerConstants.PEPPER

        hash_hex = hmac.new(ServerConstants.PEPPER, combined, hashlib.md5()).hexdigest()

        return salt.hex(), hash_hex

    @staticmethod
    def IsPasswordOK(username, password):
        return DataBase.USER_DATA[username].hashed_password == DataBase.hash_password(password)[2]

    @staticmethod
    def IsUserExist(username):
        return username in DataBase.USER_DATA.keys()