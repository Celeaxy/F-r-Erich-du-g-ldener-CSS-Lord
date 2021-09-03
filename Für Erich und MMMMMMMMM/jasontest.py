import pandas as pd
import random as r
pd.set_option('display.max_rows', None)
df = pd.read_json('data.json')
print(df["articles"][r.randint(0,len(df["articles"]))])

    


print(len(df["articles"]))
"""author": "WELT",
    "title": "China: Gericht bestätigt Todesurteil gegen Kanadier Robert Schellenberg - WELT",
    "description": "Der kanadische Drogenschmuggler Robert Lloyd Schellenberg war in China zu 15 Jahren Haft verurteilt worden. Dann wurde in Kanada jedoch die Finanzchefin des chinesischen Telekom-Riesen Huawei festgenommen. Und Schellenbergs Urteil wurde in die Todesstrafe umg…",
    "url": "https://www.welt.de/politik/ausland/article233041627/China-Gericht-bestaetigt-Todesurteil-gegen-Kanadier-Robert-Schellenberg.html",
    "urlToImage": "https://img.welt.de/img/politik/ausland/mobile233041739/2091352547-ci16x9-w1200/China-bestaetigt-Todesurteil-gegen-kanadischen-Drogenschmuggler.jpg",
    "publishedAt": "2021-08-10T09:50:35Z",
    "content"""