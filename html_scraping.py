from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

import pandas as pd
import re


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

coin_list = []

for i in range(1, 101):
    url = f"https://www.coingecko.com/?page={i}"
    driver.get(url)

    time.sleep(5)

    raw_html = driver.page_source

    #za prvo stran
    if i == 1:
        with open("page1.txt", "w", encoding="utf-8") as file:
            file.write(raw_html)

    with open("raw_html.txt", "w", encoding="utf-8") as file:
        file.write(raw_html)

   
    with open('raw_html.txt', 'r', encoding='utf-8') as file:
        html_content = file.read()

    block_pattern = re.compile(r'</td>(.*?)</tr>', re.DOTALL)
    blocks = block_pattern.findall(html_content)

    rank_pattern = re.compile(r'<td[^>]*>\s*(\d+)\s*</td>') 
    name_pattern = re.compile(r'<div[^>]*tw-text-gray-700[^>]*>(.*?)\s*<div[^>]*tw-block.*?>(.*?)</div>', re.DOTALL)
    symbol_pattern = re.compile(r'<div[^>]*tw-block[^>]*>(.*?)</div>', re.DOTALL)  
    price_pattern = re.compile(r'<span[^>]*data-price-target="price"[^>]*>(\$\s*[0-9,.]+)</span>')  
    price_change_24h_pattern = re.compile(r'data-json="\{&quot;usd&quot;:(-?\d+\.?\d*)\}"[^>]*24h[^>]*>\s*(.*?)<')
    price_change_7d_pattern = re.compile(r'data-json="\{&quot;usd&quot;:(-?\d+\.?\d*)\}"[^>]*7d[^>]*>\s*(.*?)<') 
    price_change_1h_pattern = re.compile(r'data-json="\{&quot;usd&quot;:(-?\d+\.?\d*)\}"[^>]*1h[^>]*>\s*(.*?)<')
    
    all_in_one_pattern = re.compile(r'<td[^>]*data-sort="[^"]*"[^>]*>[\s\S]*?<span[^>]*>\s*(\$\d*(?:,\d{3})*(?:\.\d{1,4})?)\s*</span>')





    for block in blocks:
     
        rank_match = rank_pattern.search(block)
        rank = rank_match.group(1) if rank_match else 'N/A'

        name_match = name_pattern.search(block)
        name = name_match.group(1).strip() if name_match else 'N/A'

        symbol_match = symbol_pattern.search(block)
        symbol = symbol_match.group(1).strip() if symbol_match else 'N/A'

        price_match = price_pattern.search(block)
        price = price_match.group(1).strip() if price_match else 'N/A'

        price_change_24h_match = price_change_24h_pattern.search(block)
        price_change_24h = price_change_24h_match.group(1).strip() if price_change_24h_match else 'N/A'

        price_change_7d_match = price_change_7d_pattern.search(block)
        price_change_7d = price_change_7d_match.group(1).strip() if price_change_7d_match else 'N/A'

        price_change_1h_match = price_change_1h_pattern.search(block)
        price_change_1h = price_change_1h_match.group(1).strip() if price_change_1h_match else 'N/A'

        mv_matches = all_in_one_pattern.findall(block)
        volume = mv_matches[1].strip() if len(mv_matches) > 1 else 'N/A'
        market_cap = mv_matches[2].strip() if len(mv_matches) > 2 else 'N/A'
        fdv = mv_matches[3].strip() if len(mv_matches) > 3 else 'N/A'

        coin = {
            'Rank': rank,
            'Name': name,
            'Symbol': symbol,
            'Price': price,
            'Market Cap': market_cap,
            'FDV': fdv,
            '24h Change (%)': price_change_24h,
            '7 Days Change (%)': price_change_7d,
            '1h Change (%)': price_change_1h,
            'Volume ($)': volume
        }

        coin_list.append(coin)

    

    with open('blocks.txt', 'w', encoding='utf-8') as output_file:
        for block in blocks:
            output_file.write(block.strip() + '\n\n')

driver.quit()

for coin in coin_list:
    print(coin)

df = pd.DataFrame(coin_list)
df.to_csv('coin_data.csv', index=False)

print("HTML je uspešno postrgan")