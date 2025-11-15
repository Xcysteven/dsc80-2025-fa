# lab.py


import os
import pandas as pd
import numpy as np
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    """
    # Don't change this function body!
    # No Python required; create the HTML file.
    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def extract_book_links(text):
    parsed_text = bs4.BeautifulSoup(text, 'lxml')

    links = []
    all_books = parsed_text.find_all('article', class_='product_pod')
    for book in all_books:
        rating_p = book.find('p', class_='star-rating')
        rating = rating_p['class'][1]  
        
        if rating not in ['Four', 'Five']:
            continue 
            
        price_p = book.find('p', class_='price_color')
        price_text = price_p.text
        
        price_float = float(price_text.replace('Â£', '').replace('£', ''))
        
        if price_float >= 50.0:
            continue  
            
        link = book.find('h3').find('a')['href']
        links.append(link)
        
    return links

def get_product_info(text, categories):
    parsed_text = bs4.BeautifulSoup(text, 'lxml')
    breadcrumb_lis = parsed_text.find('ul', class_='breadcrumb').find_all('li')
    category = breadcrumb_lis[2].find('a').text
    if category not in categories:
        return None 
    
    info_dict = {}
    info_dict['Category'] = category
    info_dict['Title'] = parsed_text.find('h1').text
    rating_p = parsed_text.find('p', class_='star-rating')
    info_dict['Rating'] = rating_p['class'][1]

    desc_header = parsed_text.find('h2', string='Product Description')
    if desc_header:
        description_p = desc_header.find_next('p')
        if description_p:
            info_dict['Description'] = description_p.text
        else:
            info_dict['Description'] = ''
    else:
        info_dict['Description'] = ''

    table = parsed_text.find('table', class_='table-striped')
    rows = table.find_all('tr')
    
    for row in rows:
        header = row.find('th').text
        value = row.find('td').text
        info_dict[header] = value
    return info_dict

def scrape_books(k, categories):
    all_books_data = []
    
    book_base_url = "http://books.toscrape.com/catalogue/"
    
    for page_num in range(1, k + 1):
        listing_url = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
        try:
            response = requests.get(listing_url)
            response.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"Stopping scrape at page {page_num}: Page not found or connection error.")
            break  
            
        page_content = response.text
        book_links = extract_book_links(page_content)
        
        for book_link in book_links:
            book_url = book_base_url + book_link
            try:
                book_response = requests.get(book_url)
                book_response.raise_for_status()
            except requests.exceptions.RequestException:
                continue  
                
            book_page_content = book_response.text
            info = get_product_info(book_page_content, categories)

            if info is not None:
                all_books_data.append(info)
    df = pd.DataFrame(all_books_data)
    return df


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def get_comments(storyid):
    session = requests.Session()
    base_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'
    
    story_resp = session.get(base_url.format(storyid))
    story_data = story_resp.json()
    
    comments_list = []

    def dfs_fetch(comment_ids):
        for cid in comment_ids:

            try:
                resp = session.get(base_url.format(cid))
                c_data = resp.json()
            except Exception:
                continue
            
            if c_data is None:
                continue

            if c_data.get('dead') or c_data.get('deleted'):
                continue
                
            comments_list.append({
                'id': c_data.get('id'),
                'by': c_data.get('by'),
                'text': c_data.get('text'),
                'parent': c_data.get('parent'),
                'time': pd.to_datetime(c_data.get('time'), unit='s')
            })
            if 'kids' in c_data:
                dfs_fetch(c_data['kids'])

    if story_data and 'kids' in story_data:
        dfs_fetch(story_data['kids'])

    df = pd.DataFrame(comments_list, columns=['id', 'by', 'text', 'parent', 'time'])
    
    return df
