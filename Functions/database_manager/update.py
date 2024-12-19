from Functions.web_scraping import get_data, get_film_data, get_serie_data
from Functions.ui_manager import update_loading, clear_terminal
from config import Texts_path
import json

with open(Texts_path, encoding="utf-8") as file:
    Texts = json.load(file)


def update(y, x, cur):

    if y == "Serie":  # serie
        data = get_serie_data(x)
        try:
            cur.execute(f"SELECT * FROM DÉJÀ_VU WHERE Code={x}")
            rows = cur.fetchall()
            rows = list(rows[0])
            data = (f"{data[0]}", f"{data[1]}", f"{data[2]}", f"{data[2]-int(rows[8])}")
        except:
            cur.execute(f"SELECT * FROM A_VOIR WHERE Code={x}")
            rows = cur.fetchall()
            rows = list(rows[0])
            data = (f"{data[0]}", f"{data[1]}", f"{data[2]}")
    else:
        data = get_film_data(x)
    return data


def update_nbr_viewed_saisons(x, con, cur):

    if con.execute(f"SELECT 1 FROM DÉJÀ_VU WHERE Code={x}").fetchone():
        cur.execute(f"SELECT * FROM DÉJÀ_VU WHERE Code={x}")
        rows = cur.fetchall()
        if list(rows[0])[1] == "Serie":
            try:
                nbr_saison_vu = int(input(Texts["qst_viewed_saisons"]))
                if nbr_saison_vu > int(list(rows[0])[7]) or nbr_saison_vu < 0:
                    1 / 0
            except:
                while True:
                    try:
                        nbr_saison_vu = int(input(Texts["err_nbr_saison"]))
                        if (
                            nbr_saison_vu <= int(list(rows[0])[7])
                            and nbr_saison_vu >= 0
                        ):
                            break
                    except:
                        pass

            nbr_saison_non_vu = int(list(rows[0])[7]) - nbr_saison_vu
            rows = list(rows[0])
            if nbr_saison_vu == 0:
                cur.execute(f"DELETE FROM SAISONS_NON_VU WHERE  Code={x} ")
                cur.execute(f"DELETE FROM DÉJÀ_VU WHERE  Code={x} ")
                del rows[8:]
                cur.execute(
                    "INSERT INTO A_VOIR(Code, Type, Titre, Image , Etat, Date, Durée, Saison) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                    rows,
                )
            elif nbr_saison_non_vu == 0:
                cur.execute(f"DELETE FROM SAISONS_NON_VU WHERE  Code={x} ")
                con.execute(
                    f"UPDATE DÉJÀ_VU SET Saison_vu = {nbr_saison_vu} WHERE Code ={x}"
                )
                con.execute(
                    f"UPDATE DÉJÀ_VU SET Saison_non_vu = {nbr_saison_non_vu} WHERE Code ={x}"
                )
            elif int(rows[9]) == 0 and nbr_saison_non_vu > 0:
                rows[8] = nbr_saison_vu
                rows[9] = nbr_saison_non_vu
                cur.execute(
                    "INSERT INTO SAISONS_NON_VU (Code, Type, Titre, Image , Etat, Date, Durée, Saison,Saison_vu, Saison_non_vu) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    rows,
                )
                con.execute(
                    f"UPDATE DÉJÀ_VU SET Saison_vu = {nbr_saison_vu} WHERE Code ={x}"
                )
                con.execute(
                    f"UPDATE DÉJÀ_VU SET Saison_non_vu = {nbr_saison_non_vu} WHERE Code ={x}"
                )
            else:
                con.execute(
                    f"UPDATE SAISONS_NON_VU SET Saison_vu = {nbr_saison_vu} WHERE Code ={x}"
                )
                con.execute(
                    f"UPDATE SAISONS_NON_VU SET Saison_non_vu = {nbr_saison_non_vu} WHERE Code ={x}"
                )
                con.execute(
                    f"UPDATE DÉJÀ_VU SET Saison_vu = {nbr_saison_vu} WHERE Code ={x}"
                )
                con.execute(
                    f"UPDATE DÉJÀ_VU SET Saison_non_vu = {nbr_saison_non_vu} WHERE Code ={x}"
                )
            print(f"{rows[1]}: '{rows[2]}' {rows[5]}, {Texts['successfully_modified']}")
            con.commit()

        else:
            print(Texts["cant_modify_movie"])
    else:
        data = get_data(x)
        print(f"{data[1]}: '{data[2]}' {data[5]}, {Texts['not_found_deja_vu']}")


def update_lists(con):
    cur = con.cursor()
    cur.execute(f"SELECT Code,Type,Saison_non_vu FROM DÉJÀ_VU ")
    rows = cur.fetchall()
    taille = len(rows)
    for i in range(0, taille):
        rows11 = list(rows[i])
        code = int(rows11[0])
        type = rows11[1]
        z = update(type, code, cur=cur)
        con.execute(f"UPDATE DÉJÀ_VU SET Etat = '{z[0]}' WHERE Code ={code}")
        con.execute(f"UPDATE DÉJÀ_VU SET Date = '{z[1]}' WHERE Code ={code}")
        if type == "Serie":
            nbr_s = int(rows11[2])
            con.execute(f"UPDATE DÉJÀ_VU SET Saison = {z[2]} WHERE Code ={code}")
            con.execute(f"UPDATE DÉJÀ_VU SET Saison_non_vu = {z[3]} WHERE Code ={code}")
            if int(z[3]) > 0 and nbr_s == 0:
                dataa = list(get_data(code))
                cur.execute(f"SELECT * FROM DÉJÀ_VU WHERE Code={code}")
                nbr_s_v = cur.fetchall()
                nbr_s_v = list(nbr_s_v[0])[8]
                dataa.append(nbr_s_v)
                dataa.append(z[3])
                print(dataa)
                cur.execute(
                    "INSERT INTO SAISONS_NON_VU (Code, Type, Titre, Image , Etat, Date, Durée, Saison,Saison_vu, Saison_non_vu) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    dataa,
                )
            con.execute(f"UPDATE SAISONS_NON_VU SET Etat = '{z[0]}' WHERE Code ={code}")
            con.execute(f"UPDATE SAISONS_NON_VU SET Date = '{z[1]}' WHERE Code ={code}")
            con.execute(
                f"UPDATE SAISONS_NON_VU SET Saison = '{z[2]}' WHERE Code ={code}"
            )
            con.execute(
                f"UPDATE SAISONS_NON_VU SET Saison_non_vu = '{z[3]}' WHERE Code ={code}"
            )
        clear_terminal()
        varp = (i / taille) * 100
        update_loading(varp, Texts["update_deja_vu"])
    cur.execute(f"SELECT Code,Type FROM A_VOIR ")
    rows = cur.fetchall()
    taille = len(rows)
    for i in range(0, taille):
        code = int(list(rows[i])[0])
        type = list(rows[i])[1]
        z = update(type, code, cur=cur)
        con.execute(f"UPDATE A_VOIR SET Etat = '{z[0]}' WHERE Code ={code}")
        con.execute(f"UPDATE A_VOIR SET Date = '{z[1]}' WHERE Code ={code}")
        if type == "Serie":
            con.execute(f"UPDATE A_VOIR SET Saison = {z[2]} WHERE Code ={code}")
        clear_terminal()
        varp = (i / taille) * 100
        update_loading(varp, Texts["update_a_voir"])
    con.commit()

    print(f"{Texts['successfully_updated']} \n\n******************\n\n")
