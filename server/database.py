import pickle
from dataclasses import dataclass

from server.server_constants import ServerConstants

@dataclass
class User:
    username: str
    password: str
    email: str

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
        DataBase.USER_DATA[username] = User(username, password, email)

        DataBase.save()
        

    @staticmethod
    def IsPasswordOK(username, password):
        return DataBase.USER_DATA[username].password == password

    @staticmethod
    def IsUserExist(username):
        return username in DataBase.USER_DATA.keys()