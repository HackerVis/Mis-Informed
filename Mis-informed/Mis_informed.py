import re
import urllib
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import threading
from newspaper import Article
from readability.readability import Document as Paper
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Take in user input for the link of the website and the keywords of the article
topic = input("Enter the article name: ")
link = input("Enter a website link: ")

# Starting Default Variables for us to interperet
informative_percent = 5
safetyResult = ''
articles = ''

# Retrieve the "Top Level Domain Type" from the given link
def get_domain_type(link):
    match = re.search(r'\.(\w+)$', link)
    if match:
        return match.group(1)
    else:
        return None

# Identify if the site type it's posted on gives or takes credibility away
def domain_percentage(top_level_domain):
    global informative_percent
    if(top_level_domain == 'com'):
        informative_percent += 4
    elif(top_level_domain == 'net'):
        informative_percent += 2
    elif(top_level_domain == 'org'):
        informative_percent += 3
    elif(top_level_domain == 'gov'):
        informative_percent += 1
    elif(top_level_domain == 'blog'):
        informative_percent += 5
    elif(top_level_domain == 'edu'):
        informative_percent += 1

# Identify if the source website is reliable
def is_domain_safe(domain_name):
    global informative_percent
    if(domain_name == "cnn"):
        informative_percent += 15
    elif(domain_name == "bbc"):
        informative_percent += 5
    elif(domain_name == "nbcnews"):
        informative_percent += 5
    elif(domain_name == "nytimes"):
        informative_percent += 5
    elif(domain_name == "foxnews"):
        informative_percent += 15
    elif(domain_name == "wsj"):
        informative_percent += 15
    elif(domain_name == "usatoday"):
        informative_percent += 15
    else:
        informative_percent += 50

# Anlyize the value of the misinformation percent
def safety_text(informative_percent):
    global safetyResult
    if(informative_percent < 25):
        safetyResult = "highly unlikely"
    elif(informative_percent < 50):
        safetyResult = "unlikely"
    elif(informative_percent >= 50):
        safetyResult = "likely"
    elif(informative_percent >= 75):
        safetyResult = "highly likely"

def alternate_articles(topic):

    news_outlets = ['cnn.com', 'bbc.com', 'foxnews.com', 'nbcnews.com']
 
    for outlet in news_outlets:
        link = "https://" + outlet + "/" + topic
        article = Article(link)
        article.download()
        article.parse()
        # Loop through each article
        if articles:
            for article in articles:
                print(article.find('h2').text)
        else:
           i += 1

    

    print("Title: ", article.title)

#    global informative_percent
#    # List of news outlets to scrape
#    news_outlets = ['cnn.com', 'bbc.com', 'foxnews.com', 'nbcnews.com']
#    i = 0
#
#    temp_percent = 0
#
#    # Loop through each news outlet
#    for outlet in news_outlets:
#        # Send GET request to website
#       #response = requests.get(f'https://www.{outlet}/search?q={topic}')
#        response = https://www.cnn.com/us/live-news/half-moon-bay-california-shooting-1-23-23/index.html
#        soup = BeautifulSoup(response.content, 'html.parser')
#        # Find all articles on the page
#        articles = soup.find_all('article')
#        # Loop through each article
#        if articles:
#            for article in articles:
#                print(article.find('h2').text)
#       else:
#           i += 1
#    informative_percent += (i * 10)

# Update the value depending on the link type .com / .net / .org, etc
top_level_domain = get_domain_type(link)

# Split the Url to give us the domain name
hostname = urlsplit(link).hostname
domain_name = ".".join(hostname.split(".")[:-1])

# Process the Likelyhood from the name of the link
domain_percentage(top_level_domain)
is_domain_safe(domain_name)
alternate_articles(topic)

# Analyze the reuslts
safety_text(informative_percent)

# Print the result of the Misinformation Analysis
print("The likelyhood of false information is ", informative_percent, "%, " + domain_name + " is " + safetyResult + " misinformation")