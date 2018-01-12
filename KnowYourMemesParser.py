
# coding: utf-8

# authors: @DmitrySerg, @FUlyankin
# repository: https://github.com/DmitrySerg/memology

import requests      # отправка запросов
import numpy as np   # матрицы, вектора и линал
import pandas as pd  # таблички и операции с ними
import time          # время

from tqdm import tqdm                 # мониторинг прогресса
from fake_useragent import UserAgent  # генерация правдоподобных юзер-агентов
from bs4 import BeautifulSoup         # очень красивый суп для обработки html

import argparse # чтение аргументов из коммандной строки

import socks   # подключение к тору
import socket
import sys


def getPageLinks(page_number):
    """
        Возвращает список ссылок на мемы, полученный с текущей страницы
        
        page_number: int/string
            номер страницы для парсинга
            
    """
    # составляем ссылку на страницу поиска
    page_link = 'http://knowyourmeme.com/memes/all/page/{}'.format(page_number)
    
    # запрашиваем данные по ней
    response = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
    
    if not response.ok:
        # если сервер нам отказал, вернем пустой лист для текущей страницы
        return [] 
    
    # получаем содержимое страницы и переводим в суп
    html = response.content
    soup = BeautifulSoup(html,'html.parser')
    
    # наконец, ищем ссылки на мемы и очищаем их от ненужных тэгов
    meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
    meme_links = ['http://knowyourmeme.com' + link.attrs['href'] for link in meme_links]
    
    return meme_links

def getStats(soup, stats):
    """
        Возвращает очищенное число просмотров/коментариев/...
        
        soup: объект bs4.BeautifulSoup 
            суп текущей страницы
            
        stats: string
            views/videos/photos/comments
            
    """

    obj = soup.find('dd', attrs={'class':stats})
    obj = obj.find('a').text
    obj = int(obj.replace(',', ''))
    
    return obj

def getProperties(soup):
    """
        Возвращает список (tuple) с названием, статусом, типом, 
        годом и местом происхождения и тэгами
        
        soup: объект bs4.BeautifulSoup 
            суп текущей страницы
    
    """
    # название - идёт с самым большим заголовком h1, легко найти
    meme_name = soup.find('section', attrs={'class':'info'}).find('h1').text.strip()
    
    # достаём все данные справа от картинки 
    properties = soup.find('aside', attrs={'class':'left'})
    
    # статус идет первым - можно не уточнять класс
    meme_status = properties.find("dd")
    # oneliner, заменяющий try-except: если тэга нет в properties, вернётся объект NoneType,
    # у которого аттрибут text отсутствует, и в этом случае он заменится на пустую строку
    meme_status = "" if not meme_status else meme_status.text.strip()
    
    # тип мема - обладает уникальным классом
    meme_type = properties.find('a', attrs={'class':'entry-type-link'})
    meme_type = "" if not meme_type else meme_type.text 
    
    # год происхождения первоисточника можно найти после заголовка Year, 
    # находим заголовок, определяем родителя и ищем следущего ребенка - наш раздел
    meme_origin_year = properties.find(text='\nYear\n')
    meme_origin_year = "" if not meme_origin_year else meme_origin_year.parent.find_next()
    meme_origin_year = meme_origin_year.text.strip()
    
    # сам первоисточник
    meme_origin_place = properties.find('dd', attrs={'class':'entry_origin_link'})
    meme_origin_place = "" if not meme_origin_place else meme_origin_place.text.strip()
    
    # тэги, связанные с мемом
    meme_tags = properties.find('dl', attrs={'id':'entry_tags'}).find('dd')
    meme_tags = "" if not meme_tags else meme_tags.text.strip()
    
    return meme_name, meme_status, meme_type, meme_origin_year, meme_origin_place, meme_tags

def getText(soup):
    """
        Возвращает текстовые описания мема
        
        soup: объект bs4.BeautifulSoup 
            суп текущей страницы
            
    """
    
    # достаём все тексты под картинкой
    body = soup.find('section', attrs={'class':'bodycopy'})
    
    # раздел about (если он есть), должен идти первым, берем его без уточнения класса
    meme_about = body.find('p')
    meme_about = "" if not meme_about else meme_about.text
    
    # раздел origin можно найти после заголовка Origin или History, 
    # находим заголовок, определяем родителя и ищем следущего ребенка - наш раздел
    meme_origin = body.find(text='Origin') or body.find(text='History')
    meme_origin = "" if not meme_origin else meme_origin.parent.find_next().text
    
    # весь остальной текст (если он есть) можно запихнуть в одно текстовое поле
    if body.text:
        other_text = body.text.strip().split('\n')[4:]
        other_text = " ".join(other_text).strip()
    else:
        other_text = ""
        
    return meme_about, meme_origin, other_text

def getMemeData(meme_page):
    """
        Запрашивает данные по странице, возвращает обработанный словарь с данными
        
        meme_page: string
            ссылка на страницу с мемом
    
    """
    
    # запрашиваем данные по ссылке
    response = requests.get(meme_page, headers={'User-Agent': UserAgent().chrome})
    
    if not response.ok:
        # если сервер нам отказал, вернем статус ошибки 
        return response.status_code
    
    # получаем содержимое страницы и переводим в суп
    html = response.content
    soup = BeautifulSoup(html,'html.parser')

    # используя ранее написанные функции парсим информацию
    views = getStats(soup=soup, stats='views')
    videos = getStats(soup=soup, stats='videos')
    photos = getStats(soup=soup, stats='photos')
    comments = getStats(soup=soup, stats='comments')

    # дата
    date = soup.find('abbr', attrs={'class':'timeago'}).attrs['title']

    # имя, статус, и т.д.
    meme_name, meme_status, meme_type, meme_origin_year, meme_origin_place, meme_tags =    getProperties(soup=soup)

    # текстовые поля
    meme_about, meme_origin, other_text = getText(soup=soup)

    # составляем словарь, в котором будут хранится все полученные и обработанные данные
    data_row = {"name":meme_name, "status":meme_status, 
                "type":meme_type, "origin_year":meme_origin_year, 
                "origin_place":meme_origin_place,
                "date_added":date, "views":views, 
                "videos":videos, "photos":photos, "comments":comments, "tags":meme_tags,
                "about":meme_about, "origin":meme_origin, "other_text":other_text}

    return data_row


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--PAGE_START', help='Choose starting page for parsing', required=True)
    parser.add_argument('--PAGE_END', help='Choose final page for parsing', required=True)
    args = parser.parse_args()

    PAGE_START = int(args.PAGE_START)
    PAGE_END = int(args.PAGE_END)


    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    final_df = pd.DataFrame(columns=['name', 'status', 'type', 'origin_year', 'origin_place',
                                     'date_added', 'views', 'videos', 'photos', 'comments', 
                                     'tags', 'about', 'origin', 'other_text'])


    for page_number in range(PAGE_START, PAGE_END):
        print("Page: {}".format(page_number))
        # собрали хрефы с текущей страницы
        for i in range(5):
            meme_links = getPageLinks(page_number)  
            if meme_links:
                break
            else:
                #print("Banned on page")
                time.sleep(20)
                
        for meme_link in meme_links:
            # иногда с первого раза страничка не парсится
            for i in range(5):
                try:
                    # пытаемся собрать по мему немного даты
                    data_row = getMemeData(meme_link)           
                    # и закидываем её в таблицу
                    final_df = final_df.append(data_row, ignore_index=True)  
                    # если всё получилось - выходим из внутреннего цикла
                    break
                except:
                    # Иначе, пробуем еще несколько раз, пока не закончатся попытки
                    #print("Banned on meme")
                    time.sleep(20) 
                    continue
        final_df.to_csv('MEMES_{}_{}.csv'.format(PAGE_START, PAGE_END))