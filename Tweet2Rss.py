import urllib.request
from bs4 import BeautifulSoup


__version__ = '0.1-SNAPSHOT'
__author__ = "Eric"
TWITTER_BASE_URL = 'https://twitter.com/'


class FuckingTweet:
    """
    Class representig a fucking tweet
    """

    def __init__(self, tweet, date, author_name, author_account):
        self.date = date
        self.tweet = tweet
        self.author_name = author_name
        self.author_account = author_account

    def __str__(self):
        return "{} par {} [{}] le {}".format(self.tweet, self.author_name, self.author_account, self.date)


class ShittyMain:
    """
    Shitty temporary main class
    """
    def __init__(self):
        self.tweets = []

    def parse(self, twitter_account):
        with urllib.request.urlopen(TWITTER_BASE_URL + twitter_account) as f:
            response = f.read().decode('utf-8')

        soup = BeautifulSoup(response, 'html.parser')
        l = soup.findAll('div', attrs={'class': 'original-tweet'})
        for text in l:
            tweet = text.find('p', attrs={'class': 'tweet-text'}).get_text()
            time = text.find('a', attrs={'class': 'tweet-timestamp'})['title']
            author = text.find('strong', attrs={'class': 'fullname'}).get_text()
            username = text.find('span', attrs={'class': 'username'}).get_text()

            self.tweets.append(FuckingTweet(tweet, time, author, username))


if __name__ == "__main__":
    m = ShittyMain()
    m.parse('CanardPCRedac')
    for t in m.tweets:
        print(t)
        print("---")



