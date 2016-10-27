#!/usr/bin/env python3

import datetime
import urllib.request
from urllib.error import HTTPError

import cherrypy
from bs4 import BeautifulSoup
from jinja2 import Template

__author__ = "Eric \"Fistons\""
__copyright__ = "Copyright 2016"
__license__ = "MIT License"
__version__ = "1.0-SNAPSHOT"
__status__ = "prototype"

TEMPLATE_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
    <channel>
        <title>Tweets of {{ tweet_account }}</title>
        <description>Tweets of {{ tweet_account }}</description>
        <link>https://twitter.com/{{ tweet_acccount }}</link>
        {% for tweet in tweets %}
        <item>
            <title><![CDATA[ {{ tweet.tweet }} ]]></title>
            <link>{{ tweet.link }}</link>
            <pubDate>{{ tweet.date }}</pubDate>
            <guid>{{ tweet.id }}</guid>
            <description><![CDATA[ {{ tweet.tweet }} ]]></description>
            {% for img in tweet.images %}
                <media:group>
                    <media:content url="{{ img }}" medium="image" type="image/jpeg"/>
                </media:group>
            {% endfor %}
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

    def __init__(self, tweet_id, tweet, date, author_name, author_account, link, is_retweet, images):
        self.is_retweet = is_retweet
        self.id = tweet_id
        self.date = date
        self.tweet = tweet
        self.author_name = author_name
        self.author_account = author_account
        self.link = link
        self.images = images

        if (self.is_retweet):
            self.tweet = "RT {} ({}): {}".format(self.author_account, self.author_name, self.tweet)

    def __str__(self):
        return "{} by {} [{}] the {} - [Id. {}] - Link: {} - is a retweet: {}".format(self.tweet, self.author_name
                                                                   , self.author_account, self.date
                                                                   , self.id, self.link
                                                                   , self.is_retweet)

class ShittyParser:
    """
    Shitty twitter html parser
    """
    TWITTER_BASE_URL = 'https://twitter.com'
    HEADERS = {'Accept-Language': "en,en_US"}
    DATE_FORMAT = "%I:%M %p - %d %b %Y"

    def __init__(self):
        self.tweets = []

    def parse(self, twitter_account):
        self.tweets.clear()
        req = urllib.request.Request(ShittyParser.TWITTER_BASE_URL + "/" + twitter_account,
                                     headers=ShittyParser.HEADERS)
        with urllib.request.urlopen(req) as f:
            response = f.read().decode('utf-8')

        soup = BeautifulSoup(response, 'html.parser')
        l = soup.findAll('div', attrs={'class': 'original-tweet'})
        for text in l:
            tweet = text.find('p', attrs={'class': 'tweet-text'}).get_text()
            time_string = text.find('a', attrs={'class': 'tweet-timestamp'})['title']
            time = datetime.datetime.strptime(time_string, ShittyParser.DATE_FORMAT)
            author = text['data-name']
            username = "@" + text['data-screen-name']
            tweet_id = text['data-tweet-id']
            link = ShittyParser.TWITTER_BASE_URL + text['data-permalink-path']
            is_retweet = text.has_attr('data-retweet-id')
            images = []
            for img in text.parent.find_all("img", attrs={'class': None}):
                images.append(img['src'])
            self.tweets.append(FuckingTweet(tweet_id, tweet, time, author, username, link, is_retweet, images))
                
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
