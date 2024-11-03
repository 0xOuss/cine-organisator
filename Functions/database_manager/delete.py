import  os
from config import  A_voir_path, Deja_vu_path, Texts_path
from Functions.web_scraping import get_data
import json 

A_voir_path=os.path.dirname(__file__).rsplit('/', 2)[0]+A_voir_path
Deja_vu_path=os.path.dirname(__file__).rsplit('/', 2)[0]+Deja_vu_path
Texts_path=os.path.dirname(__file__).rsplit('/', 2)[0]+Texts_path

with open(Texts_path) as file:
    Texts = json.load(file)




def delete_from_a_voir(x, cur):
    cur.execute(f"DELETE FROM A_VOIR WHERE  Code={x} ")
    os.system(f"rm {A_voir_path}/{x}.jpg")
    os.system("clear")
    info=get_data(x)
    print(f"{info[1]}: '{info[2]}' {info[5]}, {Texts["successfully_deleted_a_voir"]}\n\n******************\n\n")

def delete_from_deja_vu(x, cur):
    cur.execute(f"DELETE FROM DÉJÀ_VU WHERE  Code={x} ")
    os.system(f"rm {Deja_vu_path}/{x}.jpg")
    try:
        cur.execute(f"DELETE FROM SAISONS_NON_VU WHERE  Code={x} ") 
    except:
        pass
    os.system("clear")
    info=get_data(x)
    print(f"{info[1]}: '{info[2]}' {info[5]}, {Texts["successfully_deleted_deja_vu"]}\n\n******************\n\n")                #os.system("clear")

def delete(x, con, cur):
    if con.execute(f"SELECT 1 FROM A_VOIR WHERE Code={x}").fetchone():
        delete_from_a_voir(x, cur)
    elif con.execute(f"SELECT 1 FROM DÉJÀ_VU WHERE Code={x}").fetchone():
        delete_from_deja_vu(x, cur)
    else:
        info=get_data(x)
        print(f"{info[1]}: '{info[2]}' {info[5]}, {Texts["not_found"]}\n\n******************\n\n")
    con.commit()