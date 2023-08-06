import numpy as np 
import re
import string

class Tweet:
    def __init__(self, string):
        self.string = string
        
    def __str__(self):
        return self.string
    
    def remove(self, tokens):
        new_text = self.string
        for token in tokens:
            new_text = new_text.replace(token, '')
        return Tweet(new_text)
    
    def clean(self, exclude=None):
        if exclude is None:
            exclude = []
        new_text = self.lower().whitespace()
        if 'mention' not in exclude:
            new_text = new_text.remove(new_text.mention())
        if 'urls' not in exclude:
            new_text = new_text.remove(new_text.urls())
        if 'hashtag' not in exclude:
            new_text = new_text.remove(new_text.hashtag())
        if 'html' not in exclude:
            new_text = new_text.remove(new_text.html())
        if 'emoji' not in exclude:
            new_text = new_text.remove(new_text.emoji())
        if 'punct' not in exclude:
            new_text = new_text.remove(string.punctuation)
        
        return new_text.remove_extra_spaces()
    
    def lower(self):
        new_text = self.string.lower()
        return Tweet(new_text)
    
    def whitespace(self):
        text = self.string.strip()
        text = text.replace('\n', '')
        text = text.replace('\n+', ' ')
        return Tweet(text).remove_extra_spaces()
    
    def remove_extra_spaces(self):
        words = self.string.split()
        new_text = " ".join(words)
        
        return Tweet(new_text)
    
    def mention(self):
        mentions = re.findall(r'@\w+', self.string)
        return MentionList(mentions, self)
    
    def urls(self):
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.string)
        return URLList(urls, self)
    
    def hashtag(self):
        hashtags = re.findall(r'#\w+', self.string)
        return HashtagList(hashtags, self)
    
    def html(self):
        html_tags = re.findall(r'<.*?>', self.string)
        return HtmlTagList(html_tags, self)
    
    def emoji(self):
        emojis = re.findall(u"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002500-\U00002BEF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001F926-\U0001F937\U00010000-\U0010ffff\u2640-\u2642\u2600-\u2B55\u200d\u23cf\u23e9\u231a\ufe0f\u3030]+", self.string)
        return EmojiList(emojis, self)
    
    def punct(self):
        table = str.maketrans('', '', string.punctuation)
        new_text = self.string.translate(table)
        return Tweet(new_text).whitespace()

class MentionList:
    def __init__(self, mentions, tweet):
        self.mentions = mentions
        self.tweet = tweet
        
    def __str__(self):
        return str(self.mentions)

    def __getitem__(self, index):
        return self.mentions[index]

    def count(self):
        return len(self.mentions)

    def remove(self):
        new_text = self.tweet.string
        for mention in self.mentions:
            new_text = new_text.replace(mention, '')
        return Tweet(new_text).whitespace()
    
class URLList:
    def __init__(self, urls, tweet):
        self.urls = urls
        self.tweet = tweet
    
    def __str__(self):
        return str(self.urls)
    
    def __getitem__(self, index):
        return self.urls[index]

    def count(self):
        return len(self.urls)

    def remove(self):
        new_text = self.tweet.string
        for url in self.urls:
            new_text = new_text.replace(url, '')
        return Tweet(new_text).whitespace()
    
class HashtagList:
    def __init__(self, hashtags, tweet):
        self.hashtags = hashtags
        self.tweet = tweet

    def __str__(self):
        return str(self.hashtags)
    
    def __getitem__(self, index):
        return self.hashtags[index]

    def count(self):
        return len(self.hashtags)

    def remove(self):
        new_text = self.tweet.string
        for hashtag in self.hashtags:
            new_text = new_text.replace(hashtag, '')
        return Tweet(new_text).whitespace()
    
class HtmlTagList:
    def __init__(self, html_tags, tweet):
        self.html_tags = html_tags
        self.tweet = tweet

    def __str__(self):
        return str(self.html_tags)

    def __getitem__(self, index):
        return self.html_tags[index]

    def count(self):
        return len(self.html_tags)

    def remove(self):
        new_text = self.tweet.string
        for html_tag in self.html_tags:
            new_text = new_text.replace(html_tag, '')
        return Tweet(new_text).whitespace()
    
class EmojiList:
    def __init__(self, emojis, tweet):
        self.emojis = emojis
        self.tweet = tweet

    def __str__(self):
        return str(self.emojis)

    def __getitem__(self, index):
        return self.emojis[index]

    def count(self):
        return len(self.emojis)

    def remove(self):
        new_text = self.tweet.string
        for emoji in self.emojis:
            new_text = new_text.replace(emoji, '')
        return Tweet(new_text).whitespace()