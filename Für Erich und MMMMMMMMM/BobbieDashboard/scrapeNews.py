import requests
import random as r
import json


def getNews():
    url = ("https://newsapi.org/v2/top-headlines?country=de&apiKey=c7faef8951ab4561934170103f617466")
    df = requests.get(url).json()
    #art=df["articles"][r.randint(0,len(df["articles"])-1)] random article
    with open(r'D:\Bobbie2.0\BobbieDashboard2.0-ScriptFirefox\BobbieDashboard\data.json', 'w', encoding='utf-8') as f:
        json.dump(df, f, ensure_ascii=False, indent=4)