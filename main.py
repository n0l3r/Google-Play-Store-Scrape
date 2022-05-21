import requests
from bs4 import BeautifulSoup

def get_list_apps(url):
    print("scrapping...")

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "cookie": "ANID=AHWqTUmmmZ9BsfRKBKEVsNpZCh5qKhGnpNiopMu7r_N45wqtrr4wmFQkcGkeFnKc; SID=KQiRQhRYIO25JhmRItfXRzTO_n8HMlYVzkxHgHDfjwLDGCqZC4gG7LzK-PJLBR3swXQzxA.; __Secure-1PSID=KQiRQhRYIO25JhmRItfXRzTO_n8HMlYVzkxHgHDfjwLDGCqZ8fAq0D0A0aQtSQR-j2wJRQ.; __Secure-3PSID=KQiRQhRYIO25JhmRItfXRzTO_n8HMlYVzkxHgHDfjwLDGCqZ59va7BbUADjM5M2p1CBOSw.; HSID=APPjXuCGPIh5hZ6yQ; SSID=APNJ2VtLQGsI4ZAe1; APISID=qGDU4I9J4iUf0Kf3/As8MNJkOYJZDbwvbA; SAPISID=gdgqYtYCQgdJoPDQ/AdRacz-m-lIAhPl8l; __Secure-1PAPISID=gdgqYtYCQgdJoPDQ/AdRacz-m-lIAhPl8l; __Secure-3PAPISID=gdgqYtYCQgdJoPDQ/AdRacz-m-lIAhPl8l; AEC=AakniGNdaBG1JxUco9uXNAaJ3Ceu87EQRVY9fKUlsd_xJWdW6u8Pj5Aeosg; 1P_JAR=2022-05-21-08; NID=511=VGuZgFUNMaU23KILdNTxjDrvqCAWxTifSO9blNp5JAWo1arPIH1E47TdCHJnz6R9DW5OoLsM0mQ0xi0LsZT2ApWOTVALZPc_zPexof75v--bLA0ug0Q5MP-cOh2AHd2LeeVDkW41FbKrQ67xlSUSZ90TleAjyly2HOLoo-yM0VsfR9mOzP0wR9D56stS-fzXCDeg9G-miaFWbMzDt29c_5J9jbfYqjk1uY5a3_Q94wH-OSqnjHg9vVievnF0SBq6MmT3RkFgSuQPKVg1S7WUfFWo_w-sgflcVQ3NqRbG1Ng7k4SYhkJi7IaV2HrFdbHfA8bZW3QixkTsaOZceDjfwC8sXg4SQrQo0KzWluBfdS647pmqlxkBqIlB; PLAY_ACTIVE_ACCOUNT=ICrt_XL61NBE_S0rhk8RpG0k65e0XwQVdDlvB6kxiQ8=authuser-0; _ga=GA1.3.807945619.1653148673; _gid=GA1.3.715163233.1653148673; OTZ=6514078_28_28__28_; SIDCC=AJi4QfH-lLG3xi3FkE3A_m5g5Xe6Lk__SU2bJar_EoP_s4Y4tiQnKPT1a6966xKSbV5jqFa40X8; __Secure-3PSIDCC=AJi4QfGF5t2S8boPpAR2xfyrdOKs3eEAPWXrc2iYpc-CoZXy54B9XiNgrEcYO0sMIIPMiJHIbX4",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
        "x-client-data": "CI+2yQEIorbJAQipncoBCIL0ygEIlKHLAQjb78sBCJ75ywEI5oTMAQiamswBCKmpzAEI/KrMAQjCrMwBCKWvzAEYq6nKAQ=="        

    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    seemore_btn = soup.find_all("div", class_="W9yFB")
    
    seemore_link = []
    # inside see more
    for see in seemore_btn:
        for a in see.find_all("a"):
            link = "https://play.google.com" + a.get("href")
            seemore_link.append(link)
            # print(link)
    # get link apps
    apps_link = []
    for link in seemore_link:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        apps = soup.find_all("div", class_="ImZGtf mpg5gc")
        for app in apps:
            app_link = app.find_all("div", class_="wXUyZd")
            # print(app_link)
            for a in app_link:
                for a_link in a.find_all("a"):
                    apps_link.append("https://play.google.com" + a_link.get("href"))
    return apps_link

def get_app_details(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    card = soup.find_all("div", class_="JNury Ekdcne")
    
    app_details = {}
    
    for app in card:
        # get app name
        app_details["app_name"] = app.find("h1", class_="AHFaub").text
        
        temp = []
        for val in app.find_all("span", class_="T32cc UAO9ie"):
            temp.append(val.text)
            
        # get app company
        app_details["app_company"] = temp[0]

        # get app category
        app_details["app_category"] = temp[1]

        more_info = app.find_all("div", class_="JHTxhe IQ1z0d")

        for info in more_info:
            header = info.find_all("div", class_="BgcNfc")
            val = info.find_all("span", class_="IQ1z0d")

            for i, j in zip(header, val):
                app_details[i.text] = j.text
    return app_details

if __name__ == "__main__":
    urls_category = [
        "https://play.google.com/store/apps/category/GAME_ACTION",
        "https://play.google.com/store/apps/category/GAME_ADVENTURE",
        "https://play.google.com/store/apps/category/GAME_ARCADE",
        "https://play.google.com/store/apps/category/GAME_BOARD",
        "https://play.google.com/store/apps/category/GAME_CARD",
        "https://play.google.com/store/apps/category/GAME_CASINO",
        "https://play.google.com/store/apps/category/GAME_CASUAL",
        "https://play.google.com/store/apps/category/GAME_EDUCATIONAL",
        "https://play.google.com/store/apps/category/GAME_MUSIC",
        "https://play.google.com/store/apps/category/GAME_PUZZLE",
        "https://play.google.com/store/apps/category/GAME_RACING",
        "https://play.google.com/store/apps/category/GAME_ROLE_PLAYING",
        "https://play.google.com/store/apps/category/GAME_SIMULATION",
        "https://play.google.com/store/apps/category/GAME_SPORTS",
        "https://play.google.com/store/apps/category/GAME_STRATEGY",
        "https://play.google.com/store/apps/category/GAME_TRIVIA",
        "https://play.google.com/store/apps/category/GAME_WORD",
    ]

    unique_app = []
    for url in urls_category:
        print(url)
        i = 0
        for link_app in get_list_apps(url):
            if link_app not in unique_app:
                unique_app.append(link_app)
                i+=1
        print(i)
        
    
    data = []
    for link_app in unique_app:
        details = get_app_details(link_app)
        if details != {}:
            data.append(details)

    print(data, len(data))
