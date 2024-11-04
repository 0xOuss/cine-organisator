from config import  Texts_path
import json 
from Functions.ui_manager import open_cover
from config import  A_voir_path, Deja_vu_path

with open(Texts_path, encoding='utf-8') as file:
    Texts = json.load(file)


def show_lists(rows, x):
    print(f"{Texts["there_are"]} {len(rows)} {Texts["elements"]}\n")
    if x==0:
        for i in range(0,len(rows)):
            print(f".   {list(rows[i])[0]}, {list(rows[i])[1]}: '{list(rows[i])[2]}' {list(rows[i])[4]} {Texts["on"]} {list(rows[i])[5]}\n")
    else:
        for i in range(0,len(rows)):
            print(f".   {list(rows[i])[0]}, {list(rows[i])[1]}: '{list(rows[i])[2]}' {list(rows[i])[4]} {Texts["on"]} {list(rows[i])[5]}, {Texts["saisons_to_watch1"]} {list(rows[i])[9]} {Texts["saisons_to_watch2"]}\n")   
    
    print('\n\n******************\n\n')

def select_a_voir(cur):
    cur.execute(f"SELECT * FROM A_VOIR")
    rows = cur.fetchall()
    show_lists(rows, 0)

def select_deja_vu(cur):
    cur.execute(f"SELECT * FROM DÉJÀ_VU")
    rows = cur.fetchall()
    show_lists(rows, 0)

def select_saisons_non_vues(cur):
    cur.execute(f"SELECT * FROM SAISONS_NON_VU")
    rows = cur.fetchall()
    show_lists(rows, 1)


def select_element_a_voir(x,cur):
    cur.execute(f"SELECT * FROM A_VOIR WHERE Code={x}")
    rows = cur.fetchall()
    rows=list(rows[0])
    print(f"'{rows[2]}',  {Texts["info_added_a_voir"]}\n\n{rows[1]}: '{rows[2]}' {rows[4]} {rows[5]}\nCode: {rows[0]}\n{Texts["state"]}: {rows[4]}\n{Texts["duration"]}: {rows[6]}\n{Texts["nbr_saisons"]}: {rows[7]}\n\n******************\n\n")
    open_cover(f"{A_voir_path}/{rows[0]}.jpg")

def select_element_deja_vu(x,cur):
    cur.execute(f"SELECT * FROM DÉJÀ_VU WHERE Code={x}")
    rows = cur.fetchall()
    rows=list(rows[0])
    print(f"'{rows[2]}',  {Texts["info_added_deja_vu"]}\n\n{rows[1]}: '{rows[2]}' {rows[4]} {rows[5]}\nCode: {rows[0]}\n{Texts["state"]}: {rows[4]}\n{Texts["duration"]}: {rows[6]}\n{Texts["nbr_saisons"]}: {rows[7]}\n{Texts["nbr_saisons_viewed"]}: {rows[8]}\n{Texts["nbr_saisons_not_viewed"]}: {rows[9]}\n\n******************\n\n")
    open_cover(f"{Deja_vu_path}/{rows[0]}.jpg")

def check_existence_a_voir(x, con):
    return con.execute(f"SELECT 1 FROM A_VOIR WHERE Code={x}").fetchone()

def check_existence_deja_vu(x, con):
    return con.execute(f"SELECT 1 FROM DÉJÀ_VU WHERE Code={x}").fetchone()
