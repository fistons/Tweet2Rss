#!/usr/bin/env python3
"""
Main module
"""
import datetime
import urllib.request
from urllib.error import HTTPError
import re

import cherrypy
from bs4 import BeautifulSoup
from jinja2 import Template


__author__ = "Eric \"Fistons\""
__copyright__ = "Copyright 2017"
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
            <title><![CDATA[ {{ tweet.tweet_title }} ]]></title>
            <link>{{ tweet.link }}</link>
            <pubDate>{{ tweet.date }}</pubDate>
            <guid>{{ tweet.tweet_id }}</guid>
            <description><![CDATA[
                 {{ tweet.tweet }}
                 <p>
                 {% for img in tweet.images %}
                    <img src="{{ img }}" alt="image"/>
                 {% endfor %}
                 </p>
                 ]]>
            </description>
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

    def __init__(self, tweet_id, tweet_title, tweet, date, author_name,
                 author_account, link, is_retweet, images):
        self.is_retweet = is_retweet
        self.tweet_title = tweet_title
        self.tweet_id = tweet_id
        self.date = date
        self.tweet = tweet
        self.author_name = author_name
        self.author_account = author_account
        self.link = link
        self.images = images

        if self.is_retweet:
            self.tweet = "RT {} ({}): {}".format(
                self.author_account, self.author_name, self.tweet)

    def __str__(self):
        return "{} by {} [{}] the {} - [Id. {}] - Link: {} - is a retweet: {}".format(
            self.tweet, self.author_name, self.author_account,
            self.date, self.tweet_id, self.link, self.is_retweet)


class ShittyParser:
    """
    Shitty twitter html parser
    """
    TWITTER_BASE_URL = 'https://twitter.com'
    HEADERS = {'Accept-Language': "en,en_US"}
    DATE_FORMAT = "%I:%M %p - %d %b %Y"

    def __init__(self):
        self.tweets = []

    def rewrite_url(self, text):
        """
        Rewrite the url to something exploitable.
        """

        # result = re.sub(
        #    r"\b((?:https?:\/\/)?(?:www\.)?(?:[^\s.]+\.)+\w{2,4}[^\s.]+)\b",
        #    r"<a href='\1'>\1</a>", text)
        result = re.sub(
            r"(pic.twitter.com/[^ ]+)", r"<a href='https://\1'>\1</a>", text)
        return result

    def parse(self, twitter_account):
        """
        Parse the twitter html page of the account an create a rss feed with it
        """
        self.tweets.clear()
        req = urllib.request.Request(ShittyParser.TWITTER_BASE_URL + "/" + twitter_account,
                                     headers=ShittyParser.HEADERS)
        with urllib.request.urlopen(req) as stream:
            response = stream.read().decode('utf-8')

        soup = BeautifulSoup(response, 'html.parser')
        tweet_list = soup.findAll('div', attrs={'class': 'original-tweet'})
        for text in tweet_list:
            tweet_title = text.find(
                'p', attrs={'class': 'tweet-text'}).get_text(separator=u' ')
            tweet = "<p>" + self.rewrite_url(tweet_title) + "</p>"
            time_string = text.find(
                'a', attrs={'class': 'tweet-timestamp'})['title']
            time = datetime.datetime.strptime(
                time_string, ShittyParser.DATE_FORMAT)
            author = text['data-name']
            username = "@" + text['data-screen-name']
            tweet_id = text['data-tweet-id']
            link = ShittyParser.TWITTER_BASE_URL + text['data-permalink-path']
            is_retweet = text.has_attr('data-retweet-id')
            images = []
            for img in text.parent.find_all("img", attrs={'class': None}):
                images.append(img['src'])
            self.tweets.append(FuckingTweet(
                tweet_id, tweet_title, tweet,
                time, author, username, link, is_retweet, images))


class Tweet2Rss(object):
    """
    Main class
    """

    def __init__(self):
        self.parser = ShittyParser()
        self.template = Template(TEMPLATE_RSS)

    @cherrypy.expose
    def index(self):
        """
        Index
        """
        return "Usage: http://tweet2rss.exemple.com/tw/TwitterUserName"

    @cherrypy.expose(['tw'])
    def twitter(self, username):
        """
        Entry Point.
        """
        try:
            self.parser.parse(username)
            return self.template.render(tweets=self.parser.tweets, tweet_account=username)
        except HTTPError as error:
            if error.errno == 404:
                return "Unkown fucking account"
            else:
                return "Dumb twitter is down again or some retarded bullshits"


if __name__ == "__main__":
    cherrypy.config.update(CONFIG_FILE_NAME)
    cherrypy.quickstart(Tweet2Rss(), "/", CONFIG_FILE_NAME)
