import os
import webbrowser
import json 
from config import  A_voir_path, Deja_vu_path, Texts_path
from Functions.database_manager.delete import   delete, delete_from_a_voir, delete_from_deja_vu
from Functions.database_manager.insert import   add_a_voir, add_deja_vu
from Functions.database_manager.update import   update_lists, update_nbr_viewed_saisons
from Functions.database_manager.select import   check_existence_a_voir, check_existence_deja_vu, select_a_voir, select_deja_vu, select_element_a_voir, select_element_deja_vu, select_saisons_non_vues
from Functions.web_scraping import  search_url_google, get_code_and_url, get_data
from Functions.ui_manager import input_err_handling



A_voir_path=os.path.dirname(__file__).rsplit('/', 1)[0]+A_voir_path
Deja_vu_path=os.path.dirname(__file__).rsplit('/', 1)[0]+Deja_vu_path
Texts_path=os.path.dirname(__file__).rsplit('/', 1)[0]+Texts_path

with open(Texts_path) as file:
    Texts = json.load(file)


def main_menu(con, cur):

    os.system("clear")

    print(Texts["welcome1"])
    print(Texts["welcome2"])

    input_err=0                                     
    try:
        cho1=int(input(Texts["menu"]))
        if cho1==1 or cho1==2 or cho1==3 or cho1==4 or cho1==5 or cho1==0 :
            input_err=1
    except:
        input_err=0
    while input_err==0:
        try:
            cho1=int(input(Texts["try_again"]))
            if cho1==1 or cho1==2 or cho1==3 or cho1==4 or cho1==5 or cho1==0 :
                input_err=1
        except:
            input_err=0
    if cho1==0:
        os.system("clear")
        print(Texts["exit"])
        con.close()
        quit()



    while cho1!=0:
        os.system("clear")
        if cho1==1:
            while cho1==1:
                cho=input_err_handling(Texts["menu_cho1_1"], Texts["try_again"], [0,1,2,3])
                os.system("clear")
                try:
                    if cho==1 or cho==2:
                        x=input(Texts["enter_name_code"])
                        if x.isdigit() :
                            tab=get_data(x)
                        else:
                            tab=get_data(search_url_google(x))
                        os.system("clear")
                except:
                    os.system("clear")
                    print(Texts["problem_try_again"])
                    print("\n\n******************\n\n")
                    cho=3

                if cho==1:
                    add_a_voir(tab, con=con, cur=cur)
                elif cho==2:
                    add_deja_vu(tab, con=con, cur=cur)
                elif cho==3:
                    cho1=0
                else :
                    print(Texts["exit"])
                    con.close()
                    quit()
        elif cho1==2:
            x=input(Texts["enter_name_code"])
        
            try:
                if not x.isdigit():
                    x=get_code_and_url(search_url_google(x))[0]

                os.system("clear")
                delete(x , con=con, cur=cur)
            except: 
                os.system("clear")
                print(Texts["problem_try_again"])
                print("\n\n******************\n\n")
                cho=3


            
            
        elif cho1==3:
            x=input(Texts["enter_name_code"])
            while True:
                try:
                    if not x.isdigit():
                        x=get_code_and_url(search_url_google(x))[0]
                    break
                except: 
                    x=input(Texts["err_enter_name_code"])
            os.system("clear")
            if check_existence_a_voir(x, con=con):
                select_element_a_voir(x,cur=cur)
                cho=input_err_handling(Texts["menu_cho1_3_a_voir"], Texts["try_again"], [0,1,2,3])
                os.system("clear")
                if cho==1:
                    add_deja_vu(get_data(x), con=con, cur=cur)
                elif cho==2:
                    delete_from_a_voir(x, cur=cur)
                elif cho==3:
                    cho1=0
                else :
                    print(Texts["exit"])
                    con.close()
                    quit()
                
            elif check_existence_deja_vu(x, con=con):
                select_element_deja_vu(x,cur=cur)
                cho=input_err_handling(Texts["menu_cho1_3_deja_vu"], Texts["try_again"], [0,1,2,3,4])
                os.system("clear")
                if cho==1:
                    add_a_voir(get_data(x), con=con, cur=cur)
                elif cho==2:
                    delete_from_deja_vu(x, cur=cur)
                elif cho==3:
                    update_nbr_viewed_saisons(x, con=con, cur=cur)
                    print('\n\n******************\n\n')
                    
                elif cho==4:
                    cho1=0
                else :
                    print(Texts["exit"])
                    con.close()
                    quit()
                
                
            else:
                try:
                    tab=get_data(x)
                    print(f"'{tab[2]}',  {Texts["not_yet_added"]}\n\n{tab[1]}: '{tab[2]}' {tab[4]} {Texts["on"]} {tab[5]}\nCode: {tab[0]}\n{Texts["state"]}: {tab[4]}\n{Texts["duration"]}: {tab[6]}\n{Texts["nbr_saisons"]}: {tab[7]}")
                    
                    webbrowser.open(tab[3])

                    cho=input_err_handling(Texts["menu_cho1_3_not_yet_added"], Texts["try_again"], [1,2,3])
                    os.system("clear")

                    if cho==1:
                        add_a_voir(tab, con=con, cur=cur)
                        
                    elif cho==2:
                        add_deja_vu(tab, con=con, cur=cur)
                    else :
                        pass
                except:
                    print(Texts["problem_try_again"])
                    con.close()
                    quit()
            con.commit()
            
        elif cho1==4:
            while cho1==4:
                cho=input_err_handling(Texts["menu_cho1_4"], Texts["try_again"], [0,1,2,3,4])
                os.system("clear")
                if cho==1:
                    select_a_voir(cur=cur)
                elif cho==2:
                    select_deja_vu(cur=cur)
                elif cho==3:
                    select_saisons_non_vues(cur=cur)
                elif cho==4:
                    cho1=0
                else:
                    print(Texts["exit"])
                    con.close()
                    quit()
        elif cho1==5:
            while cho1==5:
                cho=input_err_handling(Texts["menu_cho1_5"], Texts["try_again"], [0,1,2,3])
                os.system("clear")
                if cho==1:
                    x=input(Texts["enter_name_code"])
                    while True:
                        try:
                            if not x.isdigit():
                                x=get_code_and_url(search_url_google(x))[0]
                            break
                        except: 
                            x=input(Texts["err_enter_name_code"])
                    os.system("clear")
                    update_nbr_viewed_saisons(x, con=con, cur=cur)
                    print('\n\n******************\n\n')
                elif cho==2:
                    update_lists(con=con) 
                elif cho==3:
                    cho1=0
                else:
                    print(Texts["exit"])
                    con.close()
                    quit()

            
        cho1=input_err_handling(Texts["menu"], Texts["try_again"], [0,1,2,3,4,5])  
        
    os.system("clear")
    print(Texts["exit"])
    con.close()
    quit()