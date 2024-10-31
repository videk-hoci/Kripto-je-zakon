# Analiza kripto trga

## Uvod
Za projektno nalogo pri predmetu Uvod v programiranje sem se odločil, da bom analiziral kripto trg s pomočjo spletne strani CoinGecko. 

## Struktura naloge

### 1. Webscrape
Datoteka `html_scraping.py`:
1. Iz spletne strani https://www.coingecko.com/ izvleče HTML s poljubnega števila strani in jih uredi v slovar coin_list
2. coin_list pretvori v CSV datoteko `coin_list.csv`
3. posebej shrani prvo stran v `page1.txt` (za možno dodatno obdelavo) in zadnjo stran zanke v `raw_html.txt` ter kovance v `blocks.txt`.

### 2. Analiza podatkov
Analiza podatkov poteka v `analiza.ipynb` in se osredotoča na naslednje podatke:
- Rank, ki je neposredno povezan z Market Cap-om
- Fully Diluted Valuation (FDV)
- Volumen
- Price Change (1h, 24h, 1 day)

Iz prve strani `page1.txt` lahko izluščimo še dodatno podatke:
- Market Cap celotnega trga
- Dnevni volumen

## Uporabljene knjižnice
Za webscrape:
- selenium (webdriver, Service, By , ChromeDriverManager)
- time

Za CSV datoteko:
- csv
- pandas
- re
- matplotlib.pyplot
