#!/usr/bin/env python

import urllib.request
from bs4 import BeautifulSoup

"""
Protoype of the web app
"""

__author__ = "Eric \"Fistons\""
__copyright__ = "Copyright 2016"
__license__ = "MIT License"
__version__ = "1.0-SNAPSHOT"
__status__ = "prototype"


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
        return "{} by {} [{}] the {}".format(self.tweet, self.author_name, self.author_account, self.date)


class ShittyParser:
    """
    Shitty temporary main class
    """
    TWITTER_BASE_URL = 'https://twitter.com/'

    def __init__(self):
        self.tweets = []

    def parse(self, twitter_account):
        with urllib.request.urlopen(ShittyParser.TWITTER_BASE_URL + twitter_account) as f:
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
    m = ShittyParser()
    m.parse('CanardPCRedac')
    for t in m.tweets:
        print(t)
        print("---")



