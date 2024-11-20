import json
import time
from bs4 import BeautifulSoup
import requests, lxml 
import datetime
import csv 



def get_data():

    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    
    with open(f'chitai_gorod_{cur_time}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(
            (
                "Название книги",
                "Цена книги",
                "Автор",
                "В наличие"
            )
        )
        
    headers = {
                "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"
    }
    
    url = "https://www.chitai-gorod.ru/search?phrase=python"    
    
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    pages_count = int(soup.find('div',class_ ="pagination__wrapper").find_all(class_ = 'pagination__text')[-1].text)
    
    books_data = []
    
    for page in range(1, pages_count + 1):
        url = f'https://www.chitai-gorod.ru/search?phrase=python&page={page}'
    
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
    
        books_items = soup.find('div', class_ = 'products-list')
        for item in books_items:
            try:
                book_title = item.find(class_ = 'product-title').find(class_ = 'product-title__head').text.strip()
            except: book_title = 'Нет названия'
            
            try:
                book_price = item.find(class_ = 'product-card__price product-card__row').find(class_ = 'product-price__value product-price__value--discount').text.strip().replace(' ','')
            except: book_price = 'Нет цены'
            
            try:
                book_author = item.find(class_ = 'product-title').find(class_ = 'product-title__author').text.strip()
            except: book_author = 'Нет автора'
            
            try:
                book_in_stock = item.find(class_ = 'action-button__text').text.strip()
            except: book_in_stock = 'Данная книга не продается'
                
            books_data.append(
                {
                    'book_title': book_title,
                    'book_price': book_price,
                    'book_author': book_author,
                    'book_in_stock': book_in_stock
                }
            )
        
            with open(f'chitai_gorod_{cur_time}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
            
                writer.writerow(
                    (
                    book_title,
                    book_price,
                    book_author,
                    book_in_stock
                    )
                )
        
        print(f'Обработана {page}/{pages_count}')
        time.sleep(1)
    
    with open(f'chitai_gorod_{cur_time}.json', 'w', encoding='utf-8') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)
    
    
def main():
    get_data()
    

if __name__ == '__main__':
    main()