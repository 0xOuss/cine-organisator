import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import ChromeDriver_path


def search_url_google(x):
    x = x.replace(" ", "+")
    url_recherche = f"https://www.google.com/search?q={x}+allocine"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriver_path), options=options)

    driver.get(url_recherche)
    time.sleep(2)
    first_result = driver.find_element(By.XPATH, "//div[@class='tF2Cxc']//a")
    url = first_result.get_attribute("href")
    driver.quit()
    return url


def get_code_and_url(x):
    if str(x).isdigit():
        code = int(x)
        type = code % 10
        if type == 2:
            url = f"https://www.allocine.fr/series/ficheserie_gen_cserie={int(code/10)}.html"
        else:
            url = (
                f"https://www.allocine.fr/film/fichefilm_gen_cfilm={int(code/10)}.html"
            )
        return (code, url)
    else:
        url = str(x)
        if "serie" in url:
            type = 2
        else:
            type = 1
        code = int("".join(list(filter(str.isdigit, url))))
        code = code * 10 + type
    return (code, url)


def get_data(x):
    page = requests.get(get_code_and_url(x)[1])
    soup = BeautifulSoup(page.content, "html.parser")
    soup.prettify()

    titre = soup.find("div", attrs={"class": "titlebar titlebar-page"})
    titre = titre.text

    linkphoto = ""
    for i in soup.find_all("img"):
        if "jpg" in i.get("src"):
            linkphoto = i.get("src")
        if "png" in i.get("src"):
            linkphoto = i.get("src")
    plus = linkphoto[linkphoto.find("/c") + 1 : linkphoto.find("0/") + 1]
    linkphoto = linkphoto.replace(plus, "r_1920_1080")

    duree_brut = soup.find("div", attrs={"class": "meta-body-item meta-body-info"})
    duree_brut = duree_brut.text
    duree = ""
    test = 0
    for i in duree_brut:
        if test == 1:
            if i != "\n" and i != "/" and i != "|":
                duree = duree + i
        if i == "/" or i == "|":
            test = test + 1

    date = ""
    nbr_saison = "-"
    if get_code_and_url(x)[0] % 10 == 2:  # serie
        type = "Serie"
        état, date, nbr_saison = get_serie_data(soup)

    else:
        type = "Film"
        état, date = get_film_data(soup)
    if any(chr.isdigit() for chr in duree):
        pass
    else:
        if type == "Film":
            duree = "inconnu"
        else:
            duree = "30-50 min"
    data = (
        f"{get_code_and_url(x)[0]}",
        f"{' '.join(type.split())}",
        f"{' '.join(titre.split())}",
        f"{linkphoto}",
        f"{' '.join(état.split())}",
        f"{' '.join(date.split())}",
        f"{' '.join(duree.split())}",
        f"{nbr_saison}",
    )
    return data


def get_film_data(soup):
    if type(soup).__name__ != "BeautifulSoup":  ################# get updated film data
        page = requests.get(get_code_and_url(soup)[1])
        soup = BeautifulSoup(page.content, "html.parser")
        soup.prettify()
    try:
        date = ""
        date_brut = soup.find("span", attrs={"class": "date"})
        date_brut = " ".join(date_brut.text.split())
        for i in range(len(date_brut)):
            if date_brut[i].isdigit() or date_brut[i].isalpha() or date_brut[i] == " ":
                date = date + date_brut[i]
        mois = "".join(list(filter(str.isalpha, date)))
        les_mois = [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ]
        if time.strptime(
            datetime.today().strftime("%d %m %Y"), "%d %m %Y"
        ) > time.strptime(
            date.replace(mois, str(les_mois.index(mois) + 1)), "%d %m %Y"
        ):
            état = "SORTI"
        else:
            état = "À VENIR"
    except:
        date = "Date Inconnue"
        état = "À VENIR"
    return (état, " ".join(date.split()))


def get_serie_data(soup):
    if type(soup).__name__ != "BeautifulSoup":  ############### get updated serie data
        page = requests.get(get_code_and_url(soup)[1])
        soup = BeautifulSoup(page.content, "html.parser")
        soup.prettify()
    nbr_saison = "-"
    date_brut = soup.find("div", attrs={"class": "meta-body-item meta-body-info"})
    date_brut = date_brut.text
    date = ""
    for i in date_brut:
        if i != "\n" and i != "/" and i != "|":
            date = date + i
        if i == "/" or i == "|":
            break
    try:
        nbr_saison = soup.find("a", attrs={"class": "end-section-link"})
        nbr_saison = nbr_saison.text
    except:
        nbr_saison = soup.find("div", attrs={"class": "stats-number"})
        nbr_saison = nbr_saison.text
    nbr_saison = int("".join(list(filter(str.isdigit, nbr_saison))))
    try:
        état = soup.find(
            "div",
            attrs={"class": "label label-text label-sm label-danger-full label-status"},
        )
        état = état.text
    except:
        try:
            état = soup.find(
                "div",
                attrs={
                    "class": "label label-text label-sm label-current-full label-status"
                },
            )
            état = état.text
        except:
            état = soup.find(
                "div",
                attrs={
                    "class": "label label-text label-sm label-info-full label-status"
                },
            )
            état = état.text
            nbr_saison = 0
    return (état, " ".join(date.split()), nbr_saison)
