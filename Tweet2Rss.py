#!/usr/bin/env python

import urllib.request
from urllib.error import HTTPError

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

    def __init__(self, tweet_id, tweet, date, author_name, author_account, link):
        self.id = tweet_id
        self.date = date
        self.tweet = tweet
        self.author_name = author_name
        self.author_account = author_account
        self.link = link

    def __str__(self):
        return "{} by {} [{}] the {} - [Id. {}] - Link: {}".format(self.tweet, self.author_name
                                                                   , self.author_account, self.date
                                                                   , self.id, self.link)


class ShittyParser:
    """
    Shitty twitter html parser
    """
    TWITTER_BASE_URL = 'https://twitter.com'
    HEADERS = {'Accept-Language': "en,en-US"}

    def __init__(self):
        self.tweets = []

    def parse(self, twitter_account):
        with urllib.request.urlopen(ShittyParser.TWITTER_BASE_URL + "/" + twitter_account) as f:
            response = f.read().decode('utf-8')

        soup = BeautifulSoup(response, 'html.parser')
        l = soup.findAll('div', attrs={'class': 'original-tweet'})
        for text in l:
            tweet = text.find('p', attrs={'class': 'tweet-text'}).get_text()
            time = text.find('a', attrs={'class': 'tweet-timestamp'})['title']
            author = text['data-name']
            username = "@" + text['data-screen-name']
            tweet_id = text['data-tweet-id']
            link = ShittyParser.TWITTER_BASE_URL + text['data-permalink-path']
            self.tweets.append(FuckingTweet(tweet_id, tweet, time, author, username, link))


if __name__ == "__main__":
    m = ShittyParser()
    try:
        m.parse('CanardPcRedac')
    except HTTPError:
        print("Unkown cocky twitter account")

    for t in m.tweets:
        print(t)
        print("---")

