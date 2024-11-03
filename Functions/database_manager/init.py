import sqlite3
import  os
from config import DB_path

DB_path= os.path.dirname(__file__).rsplit('/', 2)[0]+DB_path

def db_init():
    con = sqlite3.connect(DB_path)
    return con