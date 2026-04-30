#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║   BOULBOLET BOT v2 — Bolet Lakay                     ║
║   Rezilta · Tchala · PDF · Notifikasyon Push         ║
╠══════════════════════════════════════════════════════╣
║  SETUP:                                              ║
║  1. pip install pyTelegramBotAPI requests            ║
║  2. Chanje BOT_TOKEN ak ADMIN_CHAT_ID anba a         ║
║  3. python3 boulbolet_bot_v2.py                      ║
╠══════════════════════════════════════════════════════╣
║  KÒMAND ADMIN:                                       ║
║  /antre ga_midi:123 fl_swa:456 ny_midi:789           ║
║  /videyo https://youtu.be/xxx Tit Videyo             ║
║  /sendpdf NY_Lottery_Results_2022_2025.pdf           ║
║  /broadcast Mesaj ou a                               ║
║  /reset   — Efase rezilta jou a                      ║
║  /stats   — Wè kantite abòne                         ║
╚══════════════════════════════════════════════════════╝
"""

import os
import json
import io
import requests
import telebot
from datetime import datetime
from collections import Counter

# ══════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════
BOT_TOKEN    = os.environ.get("BOT_TOKEN",    "8342253855:AAF2JSt5r2jHYHORsi_l-kO0PyYXsUIF-IQ")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID", "6507304874"))
SITE_URL     = "https://boulbolet.com"
VIP_URL      = "https://boulbolet.com/vip"
YOUTUBE_URL  = "https://www.youtube.com/@bolettLakay"

# GitHub — URL dirèk pou telechaje PDF yo
GITHUB_RAW   = "https://raw.githubusercontent.com/Waldoantony/Boulboletbotgtelegram/main/"
KNOWN_PDFS   = {
    "NY": "NY_Lottery_Results_2022_2025.pdf",
    "FL": "FL_Lottery_Results_2022_2025.pdf",
    "GA": "GA_Lottery_Results_2022_2025.pdf",
}

# ══════════════════════════════════════════
# TCHALA DATA
# ══════════════════════════════════════════
TCHALA = [
    {"mo":"Labatwa","signifikasyon":"","p2":["16","69","31","43"]},
    {"mo":"Jape","signifikasyon":"","p2":["31"]},
    {"mo":"Myèl","signifikasyon":"","p2":["96","06","08","49"]},
    {"mo":"Aksidan","signifikasyon":"","p2":["96","06","05","49"]},
    {"mo":"Akouchman","signifikasyon":"","p2":["32","56","11","33"]},
    {"mo":"Achte","signifikasyon":"","p2":["55","07","76","36"]},
    {"mo":"Adiltè","signifikasyon":"","p2":["29","58","69","28"]},
    {"mo":"Zegwi","signifikasyon":"","p2":["38","11","07","17"]},
    {"mo":"Bay Tete","signifikasyon":"","p2":["19"]},
    {"mo":"Alimèt","signifikasyon":"","p2":["11","08","42"]},
    {"mo":"Altagras","signifikasyon":"","p2":["12","21"]},
    {"mo":"Anbilans","signifikasyon":"","p2":["30","37","22","42"]},
    {"mo":"Lanmou","signifikasyon":"Relasyon, kè kontan","p2":["12","41"]},
    {"mo":"Anana","signifikasyon":"","p2":["73","19","11"]},
    {"mo":"Ti Monnen Lajan","signifikasyon":"","p2":["11","78"]},
    {"mo":"Lajan Papye","signifikasyon":"","p2":["18","11","74"]},
    {"mo":"Arete","signifikasyon":"","p2":["36","13","24","25"]},
    {"mo":"Atelye","signifikasyon":"","p2":["41","47","45","73"]},
    {"mo":"Machin","signifikasyon":"Mouvman, aksyon vit","p2":["15","77","00","33"]},
    {"mo":"Avyon","signifikasyon":"Monte wo, siksè rapid","p2":["03","29","47","85","04"]},
    {"mo":"Bag Maryaj","signifikasyon":"","p2":["25","59"]},
    {"mo":"Benyen","signifikasyon":"","p2":["32","25","59"]},
    {"mo":"Bo","signifikasyon":"","p2":["23","14","22","05"]},
    {"mo":"Boul","signifikasyon":"Chans, jwèt","p2":["14","82","46","26"]},
    {"mo":"Bale","signifikasyon":"","p2":["55","03","14"]},
    {"mo":"Baton","signifikasyon":"","p2":["43","61"]},
    {"mo":"Bannann","signifikasyon":"Sante, vitalite","p2":["87","48"]},
    {"mo":"Bank","signifikasyon":"","p2":["61","15","84","14"]},
    {"mo":"Batèm","signifikasyon":"","p2":["88","69","58"]},
    {"mo":"Bato","signifikasyon":"Vwayaj sou dlo, lòt peyi","p2":["18","68"]},
    {"mo":"Batay","signifikasyon":"","p2":["78","11","19","32"]},
    {"mo":"Baza","signifikasyon":"","p2":["39","62"]},
    {"mo":"Beso","signifikasyon":"","p2":["01","36","62","72"]},
    {"mo":"Bib","signifikasyon":"","p2":["32","20"]},
    {"mo":"Bibwon","signifikasyon":"","p2":["82","94"]},
    {"mo":"Bekàn","signifikasyon":"","p2":["52","41","78"]},
    {"mo":"Bijou","signifikasyon":"","p2":["53","41","52"]},
    {"mo":"Ble","signifikasyon":"","p2":["01","79","09","83"]},
    {"mo":"Blese","signifikasyon":"","p2":["09","03","42","62"]},
    {"mo":"Bèf","signifikasyon":"Travay di, richès tè","p2":["16","76","96"]},
    {"mo":"Bwat","signifikasyon":"","p2":["81","93"]},
    {"mo":"Bokit","signifikasyon":"","p2":["49"]},
    {"mo":"Labou","signifikasyon":"","p2":["06","60","62","82"]},
    {"mo":"Balèn","signifikasyon":"","p2":["65","04","59"]},
    {"mo":"Boulanje","signifikasyon":"","p2":["03","21","32","60"]},
    {"mo":"Bourik","signifikasyon":"","p2":["53","35","91","14"]},
    {"mo":"Bous","signifikasyon":"","p2":["02","60","10","69"]},
    {"mo":"Bourèt","signifikasyon":"","p2":["41"]},
    {"mo":"Kabrit","signifikasyon":"Endependans, obstinasyon","p2":["28","82"]},
    {"mo":"Kado","signifikasyon":"","p2":["41","11","30","05"]},
    {"mo":"Kadna","signifikasyon":"","p2":["97","61","22","05"]},
    {"mo":"Kafe","signifikasyon":"","p2":["68","27","06"]},
    {"mo":"Kaye","signifikasyon":"","p2":["32"]},
    {"mo":"Kayiman","signifikasyon":"","p2":["29","90","60"]},
    {"mo":"Kana","signifikasyon":"","p2":["41","42","22"]},
    {"mo":"Kanaval","signifikasyon":"","p2":["66","67"]},
    {"mo":"Kazèn","signifikasyon":"","p2":["00","56","31"]},
    {"mo":"Katedral","signifikasyon":"","p2":["64","16","08","21"]},
    {"mo":"Sèkèy","signifikasyon":"","p2":["22","31"]},
    {"mo":"Seremoni","signifikasyon":"","p2":["02","07"]},
    {"mo":"Kap","signifikasyon":"","p2":["32","03","21","04"]},
    {"mo":"Chen","signifikasyon":"Zanmi oswa lènmi ki pre ou","p2":["42","73"]},
    {"mo":"Chèz","signifikasyon":"","p2":["63","16","73"]},
    {"mo":"Chantye","signifikasyon":"","p2":["32","85"]},
    {"mo":"Chapo","signifikasyon":"","p2":["20","28","71","11"]},
    {"mo":"Chaplè","signifikasyon":"","p2":["04","32"]},
    {"mo":"Chabon","signifikasyon":"","p2":["85","59","07","30"]},
    {"mo":"Chasè","signifikasyon":"","p2":["09","59","99"]},
    {"mo":"Chat","signifikasyon":"Traizon, sekrè","p2":["74","04","14","84"]},
    {"mo":"Chef","signifikasyon":"","p2":["22"]},
    {"mo":"Syèl","signifikasyon":"","p2":["66","89"]},
    {"mo":"Simityè","signifikasyon":"","p2":["03","13"]},
    {"mo":"Sinema","signifikasyon":"","p2":["75"]},
    {"mo":"Kleren","signifikasyon":"","p2":["49","14","40","36"]},
    {"mo":"Kle","signifikasyon":"","p2":["05","64","41"]},
    {"mo":"Klòch","signifikasyon":"","p2":["03","27","48","25"]},
    {"mo":"Klou","signifikasyon":"Pwoblèm kache, doulè","p2":["67","27","22"]},
    {"mo":"Kochon","signifikasyon":"Lajan sal, kont","p2":["58","32","22"]},
    {"mo":"Kòmès","signifikasyon":"","p2":["74","77"]},
    {"mo":"Kondui","signifikasyon":"","p2":["03","21","62"]},
    {"mo":"Konstriksyon","signifikasyon":"","p2":["32","19"]},
    {"mo":"Kòk","signifikasyon":"Viktorwa, konpetisyon","p2":["11","71","01","32"]},
    {"mo":"Kòk Batay","signifikasyon":"","p2":["11","15","64"]},
    {"mo":"Kòbya","signifikasyon":"","p2":["04","22","61"]},
    {"mo":"Kostim","signifikasyon":"","p2":["44","23","84"]},
    {"mo":"Koulèv","signifikasyon":"Ènmi kache, trayizon","p2":["39","21","72"]},
    {"mo":"Kou","signifikasyon":"","p2":["08","60"]},
    {"mo":"Kouto","signifikasyon":"","p2":["58","54","37","09"]},
    {"mo":"Krab","signifikasyon":"Lajan k ap vini sou kote","p2":["55","30"]},
    {"mo":"Krè","signifikasyon":"","p2":["28","19","46","62"]},
    {"mo":"Krapo","signifikasyon":"","p2":["28","73"]},
    {"mo":"Kreyon","signifikasyon":"","p2":["01","11"]},
    {"mo":"Kaka","signifikasyon":"","p2":["07"]},
    {"mo":"Kivèt","signifikasyon":"","p2":["30","14","64"]},
    {"mo":"Kizin","signifikasyon":"","p2":["24"]},
    {"mo":"Kwa","signifikasyon":"","p2":["10","40","33"]},
    {"mo":"Krich","signifikasyon":"","p2":["06","42","81","28"]},
    {"mo":"Kribich","signifikasyon":"","p2":["30","31","32"]},
    {"mo":"Danse","signifikasyon":"","p2":["79","08","86","39"]},
    {"mo":"Dan","signifikasyon":"","p2":["31","58","15"]},
    {"mo":"Drapo","signifikasyon":"","p2":["77","73","14","24"]},
    {"mo":"Dlo","signifikasyon":"Purifikasyon, emosyon","p2":["89","22","05","51"]},
    {"mo":"Echèl","signifikasyon":"","p2":["65","03","25","62"]},
    {"mo":"Ekri","signifikasyon":"","p2":["07","21","32"]},
    {"mo":"Pèdi","signifikasyon":"","p2":["51","54","74"]},
    {"mo":"Egliz","signifikasyon":"","p2":["95","75","18"]},
    {"mo":"Eleksyon","signifikasyon":"","p2":["68"]},
    {"mo":"Ansent","signifikasyon":"","p2":["20"]},
    {"mo":"Timoun","signifikasyon":"","p2":["04","13","25"]},
    {"mo":"Ènmi","signifikasyon":"","p2":["60","04","73","32"]},
    {"mo":"Antèman","signifikasyon":"Dèy, souvni, eritaj","p2":["09","91","10","66"]},
    {"mo":"Koulin","signifikasyon":"","p2":["62","14","96"]},
    {"mo":"Epeng","signifikasyon":"","p2":["73","06"]},
    {"mo":"Eskalye","signifikasyon":"","p2":["06","36"]},
    {"mo":"Etwal","signifikasyon":"","p2":["82","12","22","04"]},
    {"mo":"Etidye","signifikasyon":"","p2":["57","73"]},
    {"mo":"Fatra","signifikasyon":"","p2":["85","86"]},
    {"mo":"Fanm","signifikasyon":"","p2":["12","05","50","42"]},
    {"mo":"Fè Pou Pase Rad","signifikasyon":"","p2":["44","16"]},
    {"mo":"Genyen","signifikasyon":"","p2":["82","54","26"]},
    {"mo":"Gato","signifikasyon":"","p2":["52","48","50"]},
    {"mo":"Jandam","signifikasyon":"","p2":["25","50","03","49"]},
    {"mo":"Glas","signifikasyon":"","p2":["32","92","22"]},
    {"mo":"Gè","signifikasyon":"","p2":["95","36"]},
    {"mo":"Gita","signifikasyon":"","p2":["83","31","75","89"]},
    {"mo":"Rach","signifikasyon":"","p2":["36","10","32"]},
    {"mo":"Ranyon","signifikasyon":"","p2":["57","53"]},
    {"mo":"Zèb","signifikasyon":"","p2":["89","12","43"]},
    {"mo":"Gason","signifikasyon":"","p2":["19","02","11","91"]},
    {"mo":"Lopital","signifikasyon":"Rekiperasyon, swen ijan","p2":["60","42","32"]},
    {"mo":"Otèl","signifikasyon":"","p2":["42","32","44","69"]},
    {"mo":"Ougan","signifikasyon":"","p2":["37"]},
    {"mo":"Imaj","signifikasyon":"","p2":["66","79","57"]},
    {"mo":"Imakile","signifikasyon":"","p2":["50","12","08"]},
    {"mo":"Enprimri","signifikasyon":"","p2":["07","41","73","30"]},
    {"mo":"Ensidan","signifikasyon":"","p2":["04","27","61","83"]},
    {"mo":"Mo sal","signifikasyon":"","p2":["19","41","05","47"]},
    {"mo":"Enjistis","signifikasyon":"","p2":["82","61"]},
    {"mo":"Inondasyon","signifikasyon":"","p2":["32","85"]},
    {"mo":"Envazyon","signifikasyon":"","p2":["01","51","20"]},
    {"mo":"Sou","signifikasyon":"","p2":["10","32","51"]},
    {"mo":"Jalouzi","signifikasyon":"","p2":["05","22","80"]},
    {"mo":"Jaden","signifikasyon":"","p2":["41","01","32"]},
    {"mo":"Ja","signifikasyon":"","p2":["31","86"]},
    {"mo":"Jwèt","signifikasyon":"","p2":["14","52","21","62"]},
    {"mo":"Jounal","signifikasyon":"","p2":["96","21","62"]},
    {"mo":"Jij","signifikasyon":"","p2":["42","89","51"]},
    {"mo":"Jipon","signifikasyon":"","p2":["80","95"]},
    {"mo":"Kola","signifikasyon":"","p2":["16","85"]},
    {"mo":"Kodak","signifikasyon":"","p2":["86","04"]},
    {"mo":"Laboure","signifikasyon":"","p2":["01","29","41","91"]},
    {"mo":"Lenn","signifikasyon":"","p2":["04","45","78"]},
    {"mo":"Lèt","signifikasyon":"","p2":["75","72","13"]},
    {"mo":"Latrin","signifikasyon":"","p2":["05","81"]},
    {"mo":"Lave","signifikasyon":"","p2":["30","66","28"]},
    {"mo":"Legim","signifikasyon":"","p2":["47","29"]},
    {"mo":"Lesiv","signifikasyon":"","p2":["03","30"]},
    {"mo":"Lèt Ekri","signifikasyon":"","p2":["66","12"]},
    {"mo":"Lenj","signifikasyon":"","p2":["27","43","65","75"]},
    {"mo":"Lyon","signifikasyon":"","p2":["04","42"]},
    {"mo":"Li","signifikasyon":"","p2":["07","06","42"]},
    {"mo":"Kabann","signifikasyon":"Repo, sante, relasyon","p2":["57","59","46"]},
    {"mo":"Liv","signifikasyon":"","p2":["43"]},
    {"mo":"Lougawou","signifikasyon":"","p2":["37","47"]},
    {"mo":"Limyè","signifikasyon":"","p2":["28","80","42"]},
    {"mo":"Lalin","signifikasyon":"Sikliyè, sekrè, dlo","p2":["15","41","17","06"]},
    {"mo":"Linèt","signifikasyon":"","p2":["88","85","52"]},
    {"mo":"Magazen","signifikasyon":"","p2":["37","22"]},
    {"mo":"Mayi an gren","signifikasyon":"","p2":["20","18","97"]},
    {"mo":"Mayi Moulen","signifikasyon":"","p2":["27"]},
    {"mo":"Majistra","signifikasyon":"","p2":["00","50","21"]},
    {"mo":"Malad","signifikasyon":"","p2":["66","67","58","75"]},
    {"mo":"Manje","signifikasyon":"","p2":["57","40"]},
    {"mo":"Machann","signifikasyon":"","p2":["07"]},
    {"mo":"Mache","signifikasyon":"","p2":["27","25"]},
    {"mo":"Madigra","signifikasyon":"","p2":["37","11","77"]},
    {"mo":"Mato","signifikasyon":"","p2":["51","62"]},
    {"mo":"Matla","signifikasyon":"","p2":["04","03"]},
    {"mo":"Mekanik","signifikasyon":"","p2":["21","63"]},
    {"mo":"Melon","signifikasyon":"","p2":["11","82","29","62"]},
    {"mo":"Lanmè","signifikasyon":"Vwayaj lwen, richès gwo","p2":["07","18"]},
    {"mo":"Lamès","signifikasyon":"","p2":["92","93","05"]},
    {"mo":"Mèb","signifikasyon":"","p2":["20"]},
    {"mo":"Monsegnè","signifikasyon":"","p2":["78","79"]},
    {"mo":"Mòn","signifikasyon":"","p2":["12","50"]},
    {"mo":"Metrès","signifikasyon":"","p2":["13","22","00"]},
    {"mo":"Mont","signifikasyon":"","p2":["25","90","21"]},
    {"mo":"Moun mouri","signifikasyon":"","p2":["08","33","74"]},
    {"mo":"Motosiklèt","signifikasyon":"","p2":["53","21"]},
    {"mo":"Mouch","signifikasyon":"","p2":["45","25","09"]},
    {"mo":"Mouchwa","signifikasyon":"","p2":["84"]},
    {"mo":"Moustik","signifikasyon":"Anui, pwoblèm","p2":["35","96"]},
    {"mo":"Mizisyen","signifikasyon":"","p2":["39"]},
    {"mo":"Mi","signifikasyon":"","p2":["44","67"]},
    {"mo":"Milèt","signifikasyon":"","p2":["34","43"]},
    {"mo":"Miskad","signifikasyon":"","p2":["10","45","28","65"]},
    {"mo":"Ze","signifikasyon":"","p2":["60","00","13","16","75","87"]},
    {"mo":"Parapli","signifikasyon":"","p2":["27","57"]},
    {"mo":"Zwazo","signifikasyon":"Nouvèl, mesaj","p2":["47","60","27","02"]},
    {"mo":"Loray","signifikasyon":"","p2":["44","99","22","47"]},
    {"mo":"Zoranj","signifikasyon":"","p2":["44","02","40","13"]},
    {"mo":"Zouti","signifikasyon":"","p2":["29"]},
    {"mo":"Pay","signifikasyon":"","p2":["27","48","41","04"]},
    {"mo":"Pen","signifikasyon":"Bezwen bazik, manje","p2":["60","33","58","50"]},
    {"mo":"Palè","signifikasyon":"","p2":["53","09"]},
    {"mo":"Panye","signifikasyon":"","p2":["19","69","89"]},
    {"mo":"Pantalon","signifikasyon":"","p2":["88","20","77"]},
    {"mo":"Papye","signifikasyon":"","p2":["79","07"]},
    {"mo":"Papiyon","signifikasyon":"Transfòmasyon, bèl chanjman","p2":["02","94","12","35"]},
    {"mo":"Pafen","signifikasyon":"","p2":["91","23"]},
    {"mo":"Paspò","signifikasyon":"","p2":["79","15"]},
    {"mo":"Patat","signifikasyon":"","p2":["03","30"]},
    {"mo":"Pate","signifikasyon":"","p2":["89","02"]},
    {"mo":"Pyano","signifikasyon":"","p2":["98","99","29"]},
    {"mo":"Pijon","signifikasyon":"","p2":["24","15"]},
    {"mo":"Piman","signifikasyon":"","p2":["71"]},
    {"mo":"Pentad","signifikasyon":"","p2":["33","13","73"]},
    {"mo":"Pip","signifikasyon":"","p2":["56","12","17"]},
    {"mo":"Plenn","signifikasyon":"","p2":["72","21","26","43"]},
    {"mo":"Planch","signifikasyon":"","p2":["81","88"]},
    {"mo":"Plante","signifikasyon":"","p2":["97"]},
    {"mo":"Lapli","signifikasyon":"Beni, lajan ap tonbe","p2":["11","22","99","21"]},
    {"mo":"Plim","signifikasyon":"","p2":["07","22","33","18"]},
    {"mo":"Pwa","signifikasyon":"","p2":["87","19","90"]},
    {"mo":"Pwason","signifikasyon":"Benediksyon, abondans","p2":["27","18","78"]},
    {"mo":"Lapolis","signifikasyon":"","p2":["04","44"]},
    {"mo":"Pòm","signifikasyon":"","p2":["28","59"]},
    {"mo":"Pon","signifikasyon":"","p2":["12","73"]},
    {"mo":"Poul","signifikasyon":"Ti kont, kòmèrag","p2":["23","70","37"]},
    {"mo":"Prezidan","signifikasyon":"","p2":["11","26","45","79"]},
    {"mo":"Pè","signifikasyon":"","p2":["45","16"]},
    {"mo":"Pinèz","signifikasyon":"","p2":["97","99","30"]},
    {"mo":"Bouzen","signifikasyon":"","p2":["66","21"]},
    {"mo":"Radyo","signifikasyon":"","p2":["43","24"]},
    {"mo":"Rezen","signifikasyon":"","p2":["19","90","42"]},
    {"mo":"Rara","signifikasyon":"","p2":["79","97"]},
    {"mo":"Rat","signifikasyon":"","p2":["29","90","26"]},
    {"mo":"Ravèt","signifikasyon":"","p2":["48","33","30"]},
    {"mo":"Ravin","signifikasyon":"","p2":["01"]},
    {"mo":"Recho","signifikasyon":"","p2":["13"]},
    {"mo":"Reken","signifikasyon":"","p2":["45"]},
    {"mo":"Rèn","signifikasyon":"","p2":["56","31","82"]},
    {"mo":"Restoran","signifikasyon":"","p2":["68","28","78"]},
    {"mo":"Zam","signifikasyon":"Danje, pwoteksyon fòs","p2":["44","45","30"]},
    {"mo":"Richès","signifikasyon":"Abondans ap vini","p2":["50","51"]},
    {"mo":"Rido","signifikasyon":"","p2":["51","53","45"]},
    {"mo":"Rigòl","signifikasyon":"","p2":["56","85"]},
    {"mo":"Ri","signifikasyon":"","p2":["64","13"]},
    {"mo":"Rivyè klè","signifikasyon":"","p2":["19","33"]},
    {"mo":"Rivyè sal","signifikasyon":"","p2":["07","09","23"]},
    {"mo":"Wòb","signifikasyon":"","p2":["02","51","21","75"]},
    {"mo":"Wòch","signifikasyon":"","p2":["25","96","21"]},
    {"mo":"Wa","signifikasyon":"","p2":["27","56","78"]},
    {"mo":"Woz","signifikasyon":"","p2":["32","35"]},
    {"mo":"Sab","signifikasyon":"","p2":["89","97"]},
    {"mo":"Sak","signifikasyon":"","p2":["33","78"]},
    {"mo":"San","signifikasyon":"","p2":["45","61","05"]},
    {"mo":"Sandal","signifikasyon":"","p2":["09","52"]},
    {"mo":"Sosis","signifikasyon":"","p2":["08","97","22"]},
    {"mo":"Savon","signifikasyon":"","p2":["76","34","15","92"]},
    {"mo":"Sèl","signifikasyon":"","p2":["09","16","18"]},
    {"mo":"Siwo","signifikasyon":"","p2":["82","90"]},
    {"mo":"Swaf","signifikasyon":"","p2":["25","75","51"]},
    {"mo":"Solèy","signifikasyon":"Klète, siksè, jwa","p2":["61","25","33"]},
    {"mo":"Soulye","signifikasyon":"","p2":["88","11","28"]},
    {"mo":"Soup","signifikasyon":"","p2":["38","45","58"]},
    {"mo":"Sourit","signifikasyon":"","p2":["15","29","05","89"]},
    {"mo":"Soutyen","signifikasyon":"","p2":["61","06","43"]},
    {"mo":"Sik","signifikasyon":"","p2":["06"]},
    {"mo":"Sirèt","signifikasyon":"","p2":["38","51","56"]},
    {"mo":"Estati","signifikasyon":"","p2":["19","55","66"]},
    {"mo":"Tabak","signifikasyon":"","p2":["21","32","43","51"]},
    {"mo":"Rab","signifikasyon":"","p2":["37","04"]},
    {"mo":"Tablo","signifikasyon":"","p2":["17","60"]},
    {"mo":"Tanbou","signifikasyon":"","p2":["30","28"]},
    {"mo":"Tapi","signifikasyon":"","p2":["17"]},
    {"mo":"Telefòn","signifikasyon":"","p2":["70"]},
    {"mo":"Teren","signifikasyon":"","p2":["65"]},
    {"mo":"Teyat","signifikasyon":"","p2":["80","02"]},
    {"mo":"Tòl","signifikasyon":"","p2":["63"]},
    {"mo":"Tomat","signifikasyon":"","p2":["74","45"]},
    {"mo":"Tonb","signifikasyon":"","p2":["67","08"]},
    {"mo":"Tren","signifikasyon":"","p2":["73","12","70"]},
    {"mo":"Travay","signifikasyon":"Efò, pwodiksyon","p2":["54","25","78"]},
    {"mo":"Tribinal","signifikasyon":"","p2":["35","37"]},
    {"mo":"Twou","signifikasyon":"","p2":["07","09"]},
    {"mo":"Twonpèt","signifikasyon":"","p2":["32"]},
    {"mo":"Tiyo","signifikasyon":"","p2":["22","05","34"]},
    {"mo":"Izin","signifikasyon":"","p2":["19","27"]},
    {"mo":"Van","signifikasyon":"Nouvèl rapid, chanjman vit","p2":["75","86","32"]},
    {"mo":"Vòlè","signifikasyon":"","p2":["59","47","07"]},
    {"mo":"Vwayaj","signifikasyon":"Nouvo opòtinite, chanjman plas","p2":["44","61","92","16","08","21"]},
]

# ══════════════════════════════════════════
# STATE — Rezilta + Abòne
# ══════════════════════════════════════════
RESULTS = {
    "ga-midi": None, "ga-swa": None, "ga-nwit": None,
    "fl-midi": None, "fl-swa": None,
    "ny-midi": None, "ny-swa": None,
    "date": None
}

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_subscribers():
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(list(SUBSCRIBERS), f)

SUBSCRIBERS = load_subscribers()

# ══════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════
STATE_NAMES = {"ga": "🟢 Georgia", "fl": "🔵 Florida", "ny": "🟣 New York"}
DRAW_NAMES  = {"midi": "Midi", "swa": "Swa", "nwit": "Nwit"}

def is_admin(msg):
    return msg.chat.id == ADMIN_CHAT_ID

def get_fanmi(n):
    n = int(n)
    base = n % 33
    return [x for x in [base, base+33, base+66] if x <= 99]

def format_results_message():
    today = datetime.now().strftime("%A %d %B %Y")
    lines = [f"🎰 *REZILTA BOULBOLET*", f"📅 {today}", ""]
    ga, fl, ny = [], [], []
    for key, val in RESULTS.items():
        if key == "date" or val is None:
            continue
        state, draw = key.split("-")
        line = f"  ▪️ {DRAW_NAMES.get(draw, draw)}: *{val}*"
        if state == "ga": ga.append(line)
        elif state == "fl": fl.append(line)
        elif state == "ny": ny.append(line)
    if ga:
        lines += ["🟢 *GEORGIA*"] + ga + [""]
    if fl:
        lines += ["🔵 *FLORIDA*"] + fl + [""]
    if ny:
        lines += ["🟣 *NEW YORK*"] + ny + [""]
    if not any(RESULTS[k] for k in RESULTS if k != "date"):
        lines.append("_Pa gen rezilta ankò. Reponn pita!_")
    lines.append(f"📲 {SITE_URL}")
    return "\n".join(lines)

def format_tchala_entry(e):
    p2 = " · ".join(e["p2"])
    sig = f"\n📖 _{e['signifikasyon']}_" if e["signifikasyon"] else ""
    return f"🌙 *{e['mo'].upper()}*{sig}\n\n🎯 *Nimewo:* `{p2}`"

def main_menu(is_admin_user=False):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🎰 Dènye Rezilta",        callback_data="open_rezilta"),
        telebot.types.InlineKeyboardButton("🌙 Chèche Tchala",         callback_data="open_tchala"),
        telebot.types.InlineKeyboardButton("📄 PDF — New York (NY)",   callback_data="pdf_NY"),
        telebot.types.InlineKeyboardButton("📄 PDF — Florida (FL)",    callback_data="pdf_FL"),
        telebot.types.InlineKeyboardButton("📄 PDF — Georgia (GA)",    callback_data="pdf_GA"),
        telebot.types.InlineKeyboardButton("📲 Vizite Sit Nou",        url=SITE_URL),
    )
    if is_admin_user:
        markup.add(
            telebot.types.InlineKeyboardButton("━━━━ 👑 ADMIN ━━━━",           callback_data="noop"),
            telebot.types.InlineKeyboardButton("📤 Voye NY bay Tout Abòne",    callback_data="broadcast_pdf_NY"),
            telebot.types.InlineKeyboardButton("📤 Voye FL bay Tout Abòne",    callback_data="broadcast_pdf_FL"),
            telebot.types.InlineKeyboardButton("📤 Voye GA bay Tout Abòne",    callback_data="broadcast_pdf_GA"),
        )
    return markup

def fetch_pdf_from_github(filename):
    """Telechaje yon PDF depi GitHub. Retounen bytes oswa None."""
    url = GITHUB_RAW + filename
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 404:
            return None, f"Fichye `{filename}` pa jwenn sou GitHub."
        r.raise_for_status()
        return r.content, None
    except Exception as e:
        return None, f"Erè telechajman: `{e}`"

def broadcast_pdf(admin_cid, pdf_bytes, filename):
    """Voye yon PDF (bytes) bay tout abòne yo + notifikasyon push."""
    if not SUBSCRIBERS:
        bot.send_message(admin_cid, "⚠️ Pa gen abòne pou kounye a.")
        return

    caption = (
        f"📄 *BOULBOLET — Rezilta Ofisyèl*\n\n"
        f"Dokiman sa a prepare espesyalman pou ou.\n"
        f"👑 *Bolet Lakay* — boulbolet.com"
    )

    bot.send_message(admin_cid,
        f"⏳ Ap voye *{filename}* bay {len(SUBSCRIBERS)} abòne...",
        parse_mode='Markdown')

    success, failed_ids = 0, []
    for cid in list(SUBSCRIBERS):
        try:
            bot.send_document(cid,
                io.BytesIO(pdf_bytes),
                visible_file_name=filename,
                caption=caption,
                parse_mode='Markdown')
            success += 1
        except:
            failed_ids.append(cid)

    for bad in failed_ids:
        SUBSCRIBERS.discard(bad)
    if failed_ids:
        save_subscribers()

    bot.send_message(admin_cid,
        f"✅ *PDF voye avèk siksè!*\n\n"
        f"📄 Fichye: `{filename}`\n"
        f"📤 Voye: {success} abòne\n"
        f"❌ Echwe: {len(failed_ids)} (retire otomatikman)\n"
        f"👥 Total abòne aktif: {len(SUBSCRIBERS)}",
        parse_mode='Markdown')

def push_notification(text):
    """Voye yon notifikasyon push bay tout abòne yo."""
    success, failed_ids = 0, []
    for cid in list(SUBSCRIBERS):
        try:
            bot.send_message(cid, text, parse_mode='Markdown')
            success += 1
        except:
            failed_ids.append(cid)
    for bad in failed_ids:
        SUBSCRIBERS.discard(bad)
    if failed_ids:
        save_subscribers()
    return success

# ══════════════════════════════════════════
# BOT
# ══════════════════════════════════════════
bot = telebot.TeleBot(BOT_TOKEN)

# ── /start ──────────────────────────────
@bot.message_handler(commands=['start'])
def cmd_start(msg):
    SUBSCRIBERS.add(msg.chat.id)
    save_subscribers()
    name = msg.from_user.first_name or "zanmi"
    text = (
        f"👑 *Byenveni {name}!*\n"
        f"Ou kounye a abòne — ou ap resevwa rezilta ak PDF otomatikman!\n\n"
        f"🎰 *BOULBOLET BOT*\n"
        f"Rezilta · Tchala · PDF pou GA · FL · NY\n\n"
        f"⬇️ Chwazi opsyon ou anba a 👇"
    )
    bot.send_message(msg.chat.id, text,
        parse_mode='Markdown',
        reply_markup=main_menu(msg.chat.id == ADMIN_CHAT_ID))

# ── /meni ────────────────────────────────
@bot.message_handler(commands=['meni', 'menu'])
def cmd_meni(msg):
    bot.send_message(msg.chat.id, "📋 *Meni Prensipal:*",
        parse_mode='Markdown',
        reply_markup=main_menu(msg.chat.id == ADMIN_CHAT_ID))

# ── /ede ─────────────────────────────────
@bot.message_handler(commands=['ede', 'help'])
def cmd_help(msg):
    text = (
        "📋 *TOUT KÒMAND BOULBOLET BOT*\n\n"
        "🎰 *Rezilta*\n"
        "  /rezilta — Wè tout rezilta jodi a\n\n"
        "🌙 *Tchala*\n"
        "  /tchala chen — Chèche yon mo\n"
        "  /nimewo 44 — Ki mo ba ou 44?\n\n"
        "📊 *Analiz*\n"
        "  /fanmi 26 — Boul fanmi du 26\n"
        "  /cho — Top boul cho jounen an\n\n"
        "📄 *PDF*\n"
        "  /meni — Ouvri meni ak bouton PDF yo\n\n"
        "👑 *VIP*\n"
        "  /vip — Zouti VIP + Boul Rale Boul\n\n"
        "🔔 *Abònman*\n"
        "  /dezabòne — Kanpe notifikasyon yo\n\n"
        "📹 *Admin — YouTube*\n"
        "  /videyo <lyen> <tit> — Voye lyen videyo bay tout abòne\n\n"
        f"📲 {SITE_URL}"
    )
    bot.send_message(msg.chat.id, text, parse_mode='Markdown')

# ── /rezilta ─────────────────────────────
@bot.message_handler(commands=['rezilta', 'r'])
def cmd_rezilta(msg):
    bot.send_message(msg.chat.id, format_results_message(), parse_mode='Markdown')

# ── /tchala ──────────────────────────────
@bot.message_handler(commands=['tchala', 't'])
def cmd_tchala(msg):
    parts = msg.text.split(None, 1)
    if len(parts) < 2 or not parts[1].strip():
        bot.send_message(msg.chat.id,
            "🌙 *Tchala — Diksyonè Rèv*\n\nTape: `/tchala <mo>`\n\n"
            "Egzanp:\n  /tchala chen\n  /tchala dlo\n  /tchala lanmou",
            parse_mode='Markdown')
        return
    query = parts[1].strip().lower()
    matches = [e for e in TCHALA if query in e["mo"].lower()]
    if not matches:
        bot.send_message(msg.chat.id,
            f"😕 *{parts[1].strip()}* pa jwenn nan tchala.\n\nEseye yon lòt mo.",
            parse_mode='Markdown')
        return
    for e in matches[:3]:
        bot.send_message(msg.chat.id, format_tchala_entry(e), parse_mode='Markdown')

# ── /nimewo ──────────────────────────────
@bot.message_handler(commands=['nimewo', 'n'])
def cmd_nimewo(msg):
    parts = msg.text.split(None, 1)
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "Tape: `/nimewo 44`", parse_mode='Markdown')
        return
    num = parts[1].strip().zfill(2)
    matches = [e for e in TCHALA if num in e["p2"]]
    if not matches:
        bot.send_message(msg.chat.id,
            f"😕 Nimewo *{num}* pa jwenn nan tchala.", parse_mode='Markdown')
        return
    resp = f"🔢 *Nimewo {num} bay:*\n\n"
    resp += "\n\n".join(format_tchala_entry(e) for e in matches[:5])
    bot.send_message(msg.chat.id, resp, parse_mode='Markdown')

# ── /fanmi ───────────────────────────────
@bot.message_handler(commands=['fanmi', 'f'])
def cmd_fanmi(msg):
    parts = msg.text.split(None, 1)
    if len(parts) < 2:
        bot.send_message(msg.chat.id, "Tape: `/fanmi 26`", parse_mode='Markdown')
        return
    try:
        n = int(parts[1].strip())
        fam = get_fanmi(n)
        bot.send_message(msg.chat.id,
            f"👨‍👩‍👧 *Fanmi {n:02d}:*\n\n"
            f"🎯 `{'  ·  '.join(str(x).zfill(2) for x in fam)}`",
            parse_mode='Markdown')
    except:
        bot.send_message(msg.chat.id, "❌ Tape yon nimewo valid. Egzanp: `/fanmi 26`", parse_mode='Markdown')

# ── /cho ─────────────────────────────────
@bot.message_handler(commands=['cho'])
def cmd_cho(msg):
    all_nums = []
    for key, val in RESULTS.items():
        if key != "date" and val:
            all_nums.extend(val.replace("-", " ").split())
    if not all_nums:
        bot.send_message(msg.chat.id, "📊 Pa gen rezilta ankò jodi a.", parse_mode='Markdown')
        return
    counter = Counter(all_nums)
    top = counter.most_common(5)
    lines = [f"🔥 *TOP BOUL CHO JOU A:*\n"]
    for i, (num, cnt) in enumerate(top, 1):
        lines.append(f"  {i}. `{num}` — {cnt}x")
    bot.send_message(msg.chat.id, "\n".join(lines), parse_mode='Markdown')

# ── /vip ─────────────────────────────────
@bot.message_handler(commands=['vip'])
def cmd_vip(msg):
    bot.send_message(msg.chat.id,
        f"👑 *BOULBOLET VIP*\n\nAksè eksklizip ak zouti espesyal.\n\n🔗 {VIP_URL}",
        parse_mode='Markdown')

# ── /dezabòne ────────────────────────────
@bot.message_handler(commands=['dezabone', 'dezabòne', 'unsub'])
def cmd_dezabone(msg):
    SUBSCRIBERS.discard(msg.chat.id)
    save_subscribers()
    bot.send_message(msg.chat.id,
        "✅ Ou dezabòne. Tape /start pou abòne ankò.", parse_mode='Markdown')

# ══════════════════════════════════════════
# ADMIN COMMANDS
# ══════════════════════════════════════════

# ── /antre ───────────────────────────────
@bot.message_handler(commands=['antre'])
def cmd_antre(msg):
    if not is_admin(msg):
        bot.send_message(msg.chat.id, "⛔ Admin sèlman")
        return

    parts = msg.text.split()[1:]
    if not parts:
        bot.send_message(msg.chat.id,
            "📝 *Fòma:*\n`/antre ga_midi:123 fl_swa:456 ny_midi:789`\n\n"
            "*Kle disponib:*\n"
            "  `ga_midi` `ga_swa` `ga_nwit`\n"
            "  `fl_midi` `fl_swa`\n"
            "  `ny_midi` `ny_swa`",
            parse_mode='Markdown')
        return

    updated = []
    for part in parts:
        if ':' not in part:
            continue
        key, val = part.split(':', 1)
        key = key.strip().replace('_', '-').lower()
        val = val.strip()
        if key in RESULTS:
            RESULTS[key] = val
            updated.append(f"  ✅ {key}: *{val}*")

    if not updated:
        bot.send_message(msg.chat.id, "❌ Kle yo pa rekonèt. Verifye fòma a.", parse_mode='Markdown')
        return

    RESULTS["date"] = datetime.now().strftime("%Y-%m-%d")

    # Konfime ba admin
    bot.send_message(msg.chat.id,
        f"✅ *Rezilta antre:*\n\n" + "\n".join(updated),
        parse_mode='Markdown')

    # 🔔 NOTIFIKASYON PUSH bay tout abòne
    notif = format_results_message()
    notif = "🔔 *NOUVO REZILTA!*\n\n" + notif
    count = push_notification(notif)
    bot.send_message(msg.chat.id,
        f"📡 *Notifikasyon voye bay {count} abòne!*",
        parse_mode='Markdown')

# ── /sendpdf ─────────────────────────────
@bot.message_handler(commands=['sendpdf'])
def cmd_sendpdf(msg):
    if not is_admin(msg):
        bot.send_message(msg.chat.id, "⛔ Admin sèlman")
        return

    parts = msg.text.split(maxsplit=1)
    if len(parts) < 2:
        pdf_list = "\n".join(f"  `/sendpdf {v}`" for v in KNOWN_PDFS.values())
        bot.send_message(msg.chat.id,
            f"📄 *Chwazi PDF ou vle voye:*\n\n{pdf_list}",
            parse_mode='Markdown')
        return

    filename = parts[1].strip()
    if not filename.lower().endswith('.pdf'):
        filename += '.pdf'

    bot.send_message(msg.chat.id,
        f"⬇️ Ap telechaje `{filename}` depi GitHub...", parse_mode='Markdown')

    pdf_bytes, err = fetch_pdf_from_github(filename)
    if err:
        bot.send_message(msg.chat.id, f"❌ {err}", parse_mode='Markdown')
        return

    broadcast_pdf(msg.chat.id, pdf_bytes, filename)

# ── /reset ───────────────────────────────
@bot.message_handler(commands=['reset'])
def cmd_reset(msg):
    if not is_admin(msg):
        bot.send_message(msg.chat.id, "⛔ Admin sèlman")
        return
    for k in RESULTS:
        RESULTS[k] = None
    bot.send_message(msg.chat.id, "✅ Tout rezilta efase.")

# ── /broadcast ───────────────────────────
@bot.message_handler(commands=['broadcast'])
def cmd_broadcast(msg):
    if not is_admin(msg):
        bot.send_message(msg.chat.id, "⛔ Admin sèlman")
        return
    text = msg.text.replace('/broadcast', '', 1).strip()
    if not text:
        bot.send_message(msg.chat.id,
            "Tape: `/broadcast Mesaj ou a isit`", parse_mode='Markdown')
        return
    count = push_notification(f"📢 *BOULBOLET*\n\n{text}")
    bot.send_message(msg.chat.id, f"✅ Mesaj voye bay {count} abòne.")

# ── /videyo ──────────────────────────────
@bot.message_handler(commands=['videyo', 'video', 'yt'])
def cmd_videyo(msg):
    if not is_admin(msg):
        bot.send_message(msg.chat.id, "⛔ Admin sèlman")
        return

    parts = msg.text.split(maxsplit=2)
    # Parts: ['/videyo', 'https://youtu.be/...', 'Titre opsyonèl']
    if len(parts) < 2 or not parts[1].startswith("http"):
        bot.send_message(msg.chat.id,
            "📹 *Fòma:*\n"
            "`/videyo <lyen> <tit opsyonèl>`\n\n"
            "*Egzanp:*\n"
            "`/videyo https://youtu.be/abc123 Jou pou Jou — Dat pou Dat`\n\n"
            "_(Si ou pa mete tit, y ap jis wè lyen an)_",
            parse_mode='Markdown')
        return

    url   = parts[1].strip()
    titre = parts[2].strip() if len(parts) > 2 else None

    # Bati mesaj la
    if titre:
        notif = (
            f"🎬 *NOUVO VIDEYO — BOULBOLET!*\n\n"
            f"📺 *{titre}*\n\n"
            f"👇 Klike pou gade kounye a:\n"
            f"{url}\n\n"
            f"📲 {YOUTUBE_URL}"
        )
    else:
        notif = (
            f"🎬 *NOUVO VIDEYO — BOULBOLET!*\n\n"
            f"👇 Klike pou gade kounye a:\n"
            f"{url}\n\n"
            f"📲 {YOUTUBE_URL}"
        )

    # Bouton "Gade Videyo" dirèk
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("▶️ Gade Videyo", url=url))
    markup.add(telebot.types.InlineKeyboardButton("📺 Chaîne YouTube", url=YOUTUBE_URL))

    # Voye ba tout abòne
    success, failed_ids = 0, []
    for cid in list(SUBSCRIBERS):
        try:
            bot.send_message(cid, notif,
                parse_mode='Markdown',
                reply_markup=markup)
            success += 1
        except:
            failed_ids.append(cid)

    for bad in failed_ids:
        SUBSCRIBERS.discard(bad)
    if failed_ids:
        save_subscribers()

    bot.send_message(msg.chat.id,
        f"✅ *Videyo voye bay {success} abòne!*\n"
        f"❌ Echwe: {len(failed_ids)}\n"
        f"👥 Total aktif: {len(SUBSCRIBERS)}",
        parse_mode='Markdown')

# ── /stats ───────────────────────────────
@bot.message_handler(commands=['stats'])
def cmd_stats(msg):
    if not is_admin(msg):
        return
    lines = [
        f"📊 *Stats Bot*\n",
        f"👥 Abòne: {len(SUBSCRIBERS)}",
        f"📅 Dènye rezilta: {RESULTS.get('date') or 'Okenn'}",
    ]
    for k, v in RESULTS.items():
        if k != "date":
            lines.append(f"  {k}: {v or '—'}")
    bot.send_message(msg.chat.id, "\n".join(lines), parse_mode='Markdown')

# ══════════════════════════════════════════
# INLINE CALLBACKS
# ══════════════════════════════════════════
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id)
    cid = call.message.chat.id
    data = call.data

    if data == "noop":
        return

    elif data == "open_rezilta":
        bot.send_message(cid, format_results_message(), parse_mode='Markdown')

    elif data == "open_tchala":
        bot.send_message(cid,
            "🌙 *Tchala — Diksyonè Rèv*\n\nTape: `/tchala <mo>`\n\n"
            "Egzanp:\n  /tchala chen\n  /tchala dlo\n  /tchala lanmou",
            parse_mode='Markdown')

    elif data.startswith("pdf_"):
        # Abòne telechaje PDF pou tèt pa yo sèlman
        state = data.split("_")[1]
        filename = KNOWN_PDFS.get(state)
        if not filename:
            bot.send_message(cid, "❌ PDF pa rekonèt.")
            return
        bot.send_message(cid,
            f"⬇️ Ap telechaje *{filename}*... Yon ti moman 🙏",
            parse_mode='Markdown')
        pdf_bytes, err = fetch_pdf_from_github(filename)
        if err:
            bot.send_message(cid, f"❌ {err}", parse_mode='Markdown')
            return
        caption = (
            "📄 *BOULBOLET — Rezilta Ofisyèl*\n\n"
            "👑 *Bolet Lakay* — boulbolet.com"
        )
        bot.send_document(cid,
            io.BytesIO(pdf_bytes),
            visible_file_name=filename,
            caption=caption,
            parse_mode='Markdown')

    elif data.startswith("broadcast_pdf_"):
        # Admin sèlman — voye PDF bay tout abòne
        if cid != ADMIN_CHAT_ID:
            bot.send_message(cid, "⛔ Admin sèlman")
            return
        state = data.split("_")[2]
        filename = KNOWN_PDFS.get(state)
        if not filename:
            bot.send_message(cid, "❌ PDF pa rekonèt.")
            return
        bot.send_message(cid,
            f"⬇️ Ap telechaje *{filename}* depi GitHub...",
            parse_mode='Markdown')
        pdf_bytes, err = fetch_pdf_from_github(filename)
        if err:
            bot.send_message(cid, f"❌ {err}", parse_mode='Markdown')
            return
        broadcast_pdf(cid, pdf_bytes, filename)

# ══════════════════════════════════════════
# FREE TEXT — Chèche tchala otomatik
# ══════════════════════════════════════════
@bot.message_handler(func=lambda msg: not msg.text.startswith('/'))
def handle_text(msg):
    text = msg.text.strip().lower()

    # Nimewo → reverse lookup
    if text.isdigit() and 2 <= len(text) <= 4:
        num = text.zfill(2)
        matches = [e for e in TCHALA if num in e["p2"]]
        if matches:
            resp = f"🔢 *Nimewo {num} bay:*\n\n"
            resp += "\n\n".join(format_tchala_entry(e) for e in matches[:3])
            bot.send_message(msg.chat.id, resp, parse_mode='Markdown')
            return

    # Mo → tchala search
    matches = [e for e in TCHALA if text in e["mo"].lower()]
    if matches:
        for e in matches[:2]:
            bot.send_message(msg.chat.id, format_tchala_entry(e), parse_mode='Markdown')
        return

    # Default
    bot.send_message(msg.chat.id,
        "💬 Tape /ede pou wè tout kòmand yo, oswa eseye:\n"
        "  `/tchala chen` — chèche mo\n"
        "  `/rezilta` — dènye rezilta\n"
        "  `/meni` — ouvri meni ak bouton",
        parse_mode='Markdown')

# ══════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════
if __name__ == "__main__":
    print("╔══════════════════════════════════════╗")
    print("║   BOULBOLET BOT v2 — Kòmanse...      ║")
    print(f"║   {len(TCHALA)} mo tchala · {len(SUBSCRIBERS)} abòne        ║")
    print("╚══════════════════════════════════════╝")
    print(f"\n📋 Admin ID: {ADMIN_CHAT_ID}")
    print(f"🔔 Notifikasyon push: AKTIF")
    print(f"📄 GitHub PDF: {GITHUB_RAW}")
    print(f"\n▶  Kòmand pou kouri:")
    print(f"   python3 boulbolet_bot_v2.py\n")
    bot.infinity_polling()
