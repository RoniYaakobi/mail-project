__author__ = "RONI YAAKOBI"
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa


class ServerConstants:
    DB = r"C:\Users\roniy\software_engeeniering\11th\finalProject\Server\db.pkl"
    ENCRYPT_PATH = r"C:\Users\roniy\software_engeeniering\11th\finalProject\server"
    PRIVATE_PATH = os.path.join(ENCRYPT_PATH, "RSA_private.pem")
    PUBLIC_PATH = os.path.join(ENCRYPT_PATH, "RSA_public.pem")
    DH_PATH = os.path.join(ENCRYPT_PATH, "DH.pem")


    DB = r"server/db.pkl"
    PRIVATE_PATH = "server/RSA_private.pem"
    PUBLIC_PATH = "server/RSA_public.pem"
    DH_PATH = "server/DH.pem"

    IP = "0.0.0.0"
    PORT = 67
    ADDR = (IP,PORT)

    PEPPER = "PELEG"