#!/usr/bin/env python3
import os, sys
import logging
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
import requests
from bs4 import BeautifulSoup

def extract_market(soup) -> str:
    
    output = str()
    
    for idx, div in enumerate(soup.select("a.MarketCard-container")):
        root.debug(f"Filtering market data: #{idx + 1}")
        symbol = div.select_one(".MarketCard-symbol")
        position = div.select_one(".MarketCard-stockPosition")
        pct = div.select_one(".MarketCard-changesPct")
        
        output += f"{symbol.get_text().strip()}," if symbol else ','
        output += f"{position.get_text().strip().replace(',', '')}," if position else ','
        output += f"{pct.get_text().strip()}\n" if pct else '\n'
    
    return output

def extract_news(soup) -> str:
    output = str()
    
    for idx, div in enumerate(soup.select("div.LatestNews-headlineWrapper")):
        root.debug(f"Filtering news data: #{idx + 1}")
        timestamp = div.select_one(".LatestNews-timestamp")
        headline = div.select_one(".LatestNews-headline")
        
        output += f"{timestamp.get_text().strip()}," if timestamp else ','
        output += f"{headline.attrs['href']}," if headline else ','
        output += f"\"{headline.attrs['title']}\"\n" if headline else '\n'
        
    return output

if __name__ == "__main__":
    if not os.path.exists("../data/raw_data/web_data.html"):
        root.debug("web_data.html not exists")
        exit(1)
    
    with open("../data/raw_data/web_data.html", 'r') as fp:
        # html_list = fp.readlines()
        root.debug("Reading web_data.html")
        html = fp.read()
        
    soup = BeautifulSoup(html, "html.parser")

    market_data = extract_market(soup)
    news_data = extract_news(soup)

    if not os.path.exists("../data/processed_data"):
        root.debug("data/processed_data/ not exists")
        exit(1)

    with open("../data/processed_data/market_data.csv", 'w') as fp:
        root.debug("Writing market data on market_data.csv")
        fp.write(market_data)

    with open("../data/processed_data/news_data.csv", 'w') as fp:
        root.debug("Writing news data on news_data.csv")
        fp.write(news_data)
        
