# encoding は取得したページの文字コードを選択
filepath = 'test.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')

print(soup)
