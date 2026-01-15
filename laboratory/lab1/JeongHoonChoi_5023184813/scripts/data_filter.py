#!/usr/bin/env python3
import os, sys
import requests
from bs4 import BeautifulSoup

def extract_market(soup) -> str:
    output = str()
    
    for div in soup.select("a.MarketCard-container"):
        symbol = div.select_one(".MarketCard-symbol")
        position = div.select_one(".MarketCard-stockPosition")
        pct = div.select_one(".MarketCard-changesPct")
        
        output += f"{symbol.get_text().strip()}," if symbol else ','
        output += f"{position.get_text().strip()}," if position else ','
        output += f"{pct.get_text().strip()}\n" if pct else '\n'
    
    return output

def extract_news(soup) -> str:
    output = str()
    
    for div in soup.select("div.LatestNews-headlineWrapper"):
        timestamp = div.select_one(".LatestNews-timestamp")
        headline = div.select_one(".LatestNews-headline")
        
        output += f"{timestamp.get_text().strip()}," if timestamp else ','
        output += f"{headline.attrs['href']}," if headline else ','
        output += f"{headline.attrs['title']}\n" if headline else '\n'
        
    return output

if __name__ == "__main__":
    if not os.path.exists("../data/raw_data/web_data.html"):
        print("web_data.html not exists")
        exit(1)
    
    with open("../data/raw_data/web_data.html", 'r') as fp:
        # html_list = fp.readlines()
        html = fp.read()
        
    soup = BeautifulSoup(html, "html.parser")

    market_data = extract_market(soup)
    news_data = extract_news(soup)

    if not os.path.exists("../data/processed_data"):
        print("data/processed_data/ not exists")
        exit(1)

    with open("../data/processed_data/market_data.csv", 'w') as fp:
        fp.write(market_data)

    with open("../data/processed_data/news_data.csv", 'w') as fp:
        fp.write(news_data)
        
