from Functions.database_manager.init import db_init
from UI.menu import main_menu


def main():
    con = db_init()
    cur = con.cursor()
    main_menu(con, cur)


if __name__ == "__main__":
    main()
