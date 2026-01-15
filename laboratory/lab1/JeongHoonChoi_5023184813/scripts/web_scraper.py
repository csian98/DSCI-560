#!/usr/bin/env python3
import os, sys
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# playwright install firefox

def get_static(url: str) -> str:    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        print(f"Failed: requests.get({url})")
        exit(1)
        
    return response.text()

def get_dynamic(url: str, wait_string: str = None) -> str:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="load")
        if wait_string:
            page.wait_for_selector(wait_string, timeout=30000)
        
        html = page.content()
        browser.close()
        
    return html

def extract_html(soup, tag: str, class_: str) -> str:
    return soup.find(tag, class_).prettify()

if __name__ == "__main__":
    url = "https://www.cnbc.com/world/?region=world"
    
    # create new folers
    if not os.path.exists("../data/raw_data"):
        os.mkdir("../data/raw_data")

    if not os.path.exists("../data/processed_data"):
        os.mkdir("../data/processed_data")

    # html = get_static(url)
    html = get_dynamic(url, ".MarketCard-row")
    soup = BeautifulSoup(html, "html.parser")

    text1 = extract_html(soup, "div", "MarketsBanner-marketData")
    text2 = extract_html(soup, "ul", "LatestNews-list")
        
    with open("../data/raw_data/web_data.html", 'w') as fp:
        fp.write(text1)
        fp.write("\n")
        fp.write(text2)
