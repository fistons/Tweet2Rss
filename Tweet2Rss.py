import urllib.request
from bs4 import BeautifulSoup


def main():
    with urllib.request.urlopen("https://twitter.com/CanardPcRedac") as f:
        response = f.read().decode('utf-8')

    html = response
    soup = BeautifulSoup(html, 'html.parser')


if __name__ == "__main__":
    main()


