import pickle
import os
import hmac
import datetime
import random as rnd
from dataclasses import dataclass

from server.server_constants import ServerConstants



@dataclass
class User:
    username: str
    hashed_password: str
    email: str
    salt: bytes
    code: int
    expiration_date: datetime.datetime
    is_verified: bool

class DataBase:
    USER_DATA = {}

    def write_op(func):

        def wrapper(*args, **kwargs):
            val = func(*args,**kwargs)
            DataBase.save()
            return val
        
        return wrapper
    
    def read_op(func):

        def wrapper(*args, **kwargs):
            DataBase.load()
            return func(*args,**kwargs)
        
        return wrapper

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
    @read_op
    def GetUserEmail(username):
        if user := DataBase.USER_DATA.get(username, None):
            return user.email
        
        return "-1"
    
    @staticmethod
    @read_op
    def IsEmailUsed(email):
        for user in DataBase.USER_DATA.values():
            if user.email == email:
                return user.is_verified or user.expiration_date < datetime.datetime.now()
        return False
    
    @staticmethod
    @write_op
    def ValidateAccount(username, code):
        user = DataBase.USER_DATA.get(username, None)
        if DataBase.IsValidCode(user, code):
            user.is_verified = True
        return user.is_verified
    
    @staticmethod
    @read_op
    def IsValidCode(user, code):
        print(user)
        print(user.expiration_date > datetime.datetime.now())
        print(user.expiration_date, datetime.datetime.now())
        return user and user.code == int(code) and user.expiration_date > datetime.datetime.now()
    
    
    @staticmethod
    @read_op
    def IsVerified(username):
        user = DataBase.USER_DATA.get(username, None)
        return user and user.is_verified


    @staticmethod
    @write_op
    def SaveUser(username, email, password):
        salt, hashed_password = DataBase.hash_password(password)
        code = rnd.randint(1,1000)
        DataBase.USER_DATA[username] = User(username, hashed_password, email, salt,
                                            code , datetime.datetime.now() + datetime.timedelta(minutes=5), False)

        return str(code)
    
    @staticmethod
    @write_op
    def ResetCode(username):
        user = DataBase.USER_DATA.get(username, None)
        if user:
            code = rnd.randint(1,1000)
            user.code = code
            user.expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
            return code
        
        return -1

        
    @staticmethod
    def hash_password(password, salt=None):
        if not salt: 
            salt = os.urandom(16)

        print("salt: ", salt)

        combined = password.encode("utf-8") + salt + ServerConstants.PEPPER.encode()

        print("combined: ", combined)

        hash_hex = hmac.new(ServerConstants.PEPPER.encode(), combined, "md5").hexdigest()

        return salt, hash_hex

    @staticmethod
    @read_op
    def IsPasswordOK(username, password):
        salt = DataBase.USER_DATA[username].salt

        hashed_password = DataBase.USER_DATA[username].hashed_password

        return hashed_password == DataBase.hash_password(password,salt)[1]

    @staticmethod
    @read_op
    def IsUserExist(username):
        return username in DataBase.USER_DATA.keys()