#!/usr/bin/env python

import urllib.request
from urllib.error import HTTPError

import cherrypy
from bs4 import BeautifulSoup
from jinja2 import Template

"""
Prototype of the web app
"""

__author__ = "Eric \"Fistons\""
__copyright__ = "Copyright 2016"
__license__ = "MIT License"
__version__ = "1.0-SNAPSHOT"
__status__ = "prototype"

TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Tweets of {{ tweet_account }}</title>
</head>
<body>
    <ul id="navigation">
    {% for tweet in tweets %}
        <li id={{ tweet.id }}>
            <p>{{ tweet.tweet }}</p>
            <p>by {{ tweet.author_name }} [{{ tweet.author_account }}] - {{ tweet.date }}
        </li>
    {% endfor %}
    </ul>
</body>
</html>"""


TEMPLATE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>Tweets of {{ tweet_account }}</title>
        <description>Tweets of {{ tweet_account }}</description>
        <link>https://twitter.com/{{ tweet_acccount }}</link>
        {% for tweet in tweets %}
        <item>
            <title>{{ tweet.tweet }}</title>
            <link>{{ tweet.link }}</link>
            <pubDate>{{ tweet.date }}</pubDate>
            <guid>{{ tweet.id }}</guid>
            <description>{{ tweet.tweet }}</description>
        </item>
        {% endfor %}
    </channel>
</rss>
"""

CONFIG_FILE_NAME = "Tweet2Rss.conf"


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
    HEADERS = {'Accept-Language': "en,en_US"}

    def __init__(self):
        self.tweets = []

    def parse(self, twitter_account):
        self.tweets.clear()
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


class Tweet2Rss(object):
    def __init__(self):
        self.parser = ShittyParser()
        self.template = Template(TEMPLATE_RSS)

    @cherrypy.expose
    def index(self):
        return "Yeah, so?"

    @cherrypy.expose
    def tw(self, username):
        try:
            self.parser.parse(username)
            return self.template.render(tweets=self.parser.tweets, tweet_account=username)
        except HTTPError as e:
            if e.errno == 404:
                return "Unkown fucking account"
            else:
                return "Dumb twitter is down again or some retarded bullshits"


if __name__ == "__main__":
    cherrypy.config.update(CONFIG_FILE_NAME)
    cherrypy.quickstart(Tweet2Rss(), "/", CONFIG_FILE_NAME)
