import eel
from json import load
import tkinter as tk
from random import choice
from bs4 import BeautifulSoup
from requests import get
from os import path

root = tk.Tk()
d = root.winfo_screenwidth()
h = root.winfo_screenheight()
eel_height = int(0.9 * h)
eel_width = eel_height * 4 // 3
x_pos = int((d - eel_width) / 2)
y_pos = int((h - eel_height) / 2)
file_path = path.join(path.dirname(path.abspath(__file__)), 'web', 'texts.json')
file_path1 = path.join(path.dirname(path.abspath(__file__)), 'web', 'items.json')
data_texts = load(open(file_path, encoding="utf8"))
data_items = load(open(file_path1, encoding="utf8"))

chrome_paths = ["C:/Program Files/Google/Chrome/Application/chrome.exe",
                "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"]


@eel.expose
def SearchAuthors(search):
    res = []
    res = []
    words = [i.lower() for i in search.split()]
    for key, value in data_items.items():
        if search == '' or len([i for i in words if i in key.lower() or i in value[0].lower()]) == len(words):
            res.append([value[1], key, value[0]])
    return res


@eel.expose
def SearchText(name):
    data = open('web/data/' + name + '.txt', encoding="utf8")
    return ' '.join(data.readlines())


@eel.expose
def CheckRandom(question):
    item = choice(list(data_items.items()))[0]
    if question == 'type':
        return [item, data_items[item][1]]
    elif question == 'author':
        return [item, data_items[item][0]]


@eel.expose
def getText(item):
    if item[-1] == '0':
        data = data_texts[item[:-1]][int(item[-1])].split()
        html_content = BeautifulSoup(get(data[0]).text, "html.parser")
        for tag in data[1:]:
            html_content = html_content.find(tag)
        return html_content.prettify()

    elif item[-1] == '1':
        data = []
        soup = BeautifulSoup(get(data_texts[item[:-1]][int(item[-1])]).text, 'html.parser').find(
                'div').find('div').find('div').find('article')
        if item not in ['Господин из Сан-Франциско1', 'Куст сирени1']:
            soup = soup.select("h2#sub5")[0].find_all_next()
        else:
            soup = soup.select("h2#sub4")[0].find_all_next()
        for element in soup:
            if 'И что в итоге?' in element:
                break
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'p']:
                data.append(element)
        return BeautifulSoup(''.join(str(elem) for elem in data), 'html.parser').prettify()

    elif item[-1] == '2':
        data = []
        soup = BeautifulSoup(get(data_texts[item[:-1]][int(item[-1])]).text, 'html.parser').find(
                'div').find('div').find('div').find('article').select("h2#sub2")[0].find_all_next()
        for element in soup:
            if 'Посмотрите, что еще у нас есть:' in element:
                break
            if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'p']:
                try:
                    element.div.decompose()
                except:
                    pass
                data.append(element)
        return BeautifulSoup(''.join(str(elem) for elem in data), 'html.parser').prettify()


eel.init("web")
if any(path.exists(i) for i in chrome_paths):
    eel.start("main.html", size=(eel_width, eel_height), position=(x_pos, y_pos))
else:
    eel.start("main.html", mode='default')