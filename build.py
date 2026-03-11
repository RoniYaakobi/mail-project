__author__ = "RONI YAAKOBI"
import os
from os.path import join, getsize

PATH = r"C:\Users\roniy\software_engeeniering\11th\finalProject"
SIGNATURE = '__author__ = "RONI YAAKOBI"'

for root, dirs, files in os.walk(PATH):
    for file in files:
        with open(os.path.join(root, file), "r") as f:
            lines = f.readlines()
        
        if lines[0].strip() != SIGNATURE:
            with open(os.path.join(root, file), "w") as f:
                f.writelines([SIGNATURE] + lines)
                
    if '__pycache__' in dirs:
        dirs.remove('__pycache__') # don't visit __pycache__ directories