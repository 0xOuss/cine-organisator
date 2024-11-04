import  os
from config import  A_voir_path, Deja_vu_path, Texts_path
from Functions.ui_manager import clear_terminal
import json 
import requests

with open(Texts_path, encoding='utf-8') as file:
    Texts = json.load(file)



def add_a_voir(data, con, cur):
    try:
        data=list(data)
        response = requests.get(data[3])
        photo=f"{A_voir_path}/{data[0]}.jpg"
        f = open("%s" % (photo), "wb")
        f.write(response.content)
        f.close()
        
        
        try:
            os.remove(f"{Deja_vu_path}/{data[0]}.jpg")
            clear_terminal()
        except:
            pass
        try:
            cur.execute(f"DELETE FROM DÉJÀ_VU WHERE  Code={data[0]} ")
            try:
               cur.execute(f"DELETE FROM SAISONS_NON_VU WHERE  Code={data[0]} ") 
            except:
                pass
        except:
            pass 
        cur.execute("INSERT INTO A_VOIR(Code, Type, Titre, Image , Etat, Date, Durée, Saison) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", data)
        #cur.execute("CREATE TABLE IF NOT EXISTS A_VOIR(Code INT UNIQUE,Type TEXT,Titre TEXT UNIQUE, Image BLOB, Etat TEXT, Date TEXT, Durée TEXT, Saison TEXT)")
        con.commit()
        clear_terminal()
        print(f"{data[1]}: '{data[2]}' {data[5]}, {Texts['successfully_added_a_voir']} \n\n******************\n\n")
    except:
        clear_terminal()
        print(f"{data[1]}: '{data[2]}' {data[5]}, {Texts['already_added_a_voir']} \n\n******************\n\n")


def add_deja_vu(data, con, cur):
    try:
        data=list(data)
        response = requests.get(data[3])
        photo=f"{Deja_vu_path}/{data[0]}.jpg"
        f = open("%s" % (photo), "wb")
        f.write(response.content)
        f.close()

        try:
            os.remove(f"{A_voir_path}/{data[0]}.jpg")
            clear_terminal()
        except:
            pass
        
        if data[1]=="Serie":
            print(f"{data[1]}: '{data[2]}' {data[5]}, a {data[7]} {Texts['info_nbr_saisons']}\n")
            try:
                nbr_saison_vu=int(input(Texts['qst_viewed_saisons']))
                if (nbr_saison_vu>int(data[7])  or nbr_saison_vu<=0):
                    1/0
            except:
                while True:
                    try:
                        nbr_saison_vu=int(input(Texts['err_nbr_saison']))
                        if (nbr_saison_vu<=int(data[7])  and nbr_saison_vu>0):
                            break
                    except:
                        pass
            nbr_saison_non_vu=int(data[7])-nbr_saison_vu
        else:
            nbr_saison_non_vu="-"
            nbr_saison_vu="-"
        data.append(nbr_saison_vu)
        data.append(nbr_saison_non_vu)
        try:
            cur.execute(f"DELETE FROM A_VOIR WHERE  Code={data[0]} ")
        except:
            pass
        
        try: 
            if nbr_saison_non_vu>0:
                cur.execute("INSERT INTO SAISONS_NON_VU (Code, Type, Titre, Image , Etat, Date, Durée, Saison,Saison_vu, Saison_non_vu) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        except:
            pass
        cur.execute("INSERT INTO DÉJÀ_VU(Code, Type, Titre, Image , Etat, Date, Durée, Saison,Saison_vu, Saison_non_vu) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        #cur.execute("CREATE TABLE IF NOT EXISTS DÉJÀ_VU(Code INT UNIQUE,Type TEXT,Titre TEXT UNIQUE, Image BLOB, Etat TEXT, Date TEXT, Durée TEXT,  Saison TEXT,Saison_vu TEXT, Saison_non_vu TEXT)")
        con.commit()
        clear_terminal()
        print(f"{data[1]}: '{data[2]}' {data[5]}, {Texts['successfully_added_deja_vu']}\n\n******************\n\n")
    except:
        clear_terminal()
        print(f"{data[1]}: '{data[2]}' {data[5]}, {Texts['already_added_deja_vu']} '\n\n******************\n\n")
