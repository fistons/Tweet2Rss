import urllib.request
from bs4 import BeautifulSoup


__version__ = '0.1-SNAPSHOT'
TWITTER_BASE_URL = 'https://twitter.com/'


def parse(url):
    with urllib.request.urlopen(TWITTER_BASE_URL + url) as f:
        response = f.read().decode('utf-8')

    html = response
    soup = BeautifulSoup(html, 'html.parser')
    l = soup.findAll('p', attrs={'class': 'tweet-text'})
    for text in l:
        print(text)


if __name__ == "__main__":
    parse('CanardPCRedac')


