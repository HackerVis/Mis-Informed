import urllib
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import requests
from newspaper import Article
import datetime

# Take in user input for the link of the website and the keywords of the article
# link = input("Enter a website link: ")

# Starting Default Variables for us to interperet
informative_percent = 5
safetyResult = ''
articles = ''
isBlog = False

# Retrieve The Date Published of the Article
def get_date_published(link):
    global informative_percent
    article = Article(link)
    article.download()
    article.parse()

    try:
        publish_date = article.publish_date
    except AttributeError:
        publish_date = 10
    today = datetime.datetime.now()


    if publish_date != None:
        delta = today - publish_date
        years_since_publish = int(delta.days / 365)
        dates = {0 : 5, 1 : 2, 2 : 3, 3 : 4, 4 : 5}
        if (years_since_publish <= 4):
            informative_percent += dates[years_since_publish]
        else:
            informative_percent += 5
    else:
        informative_percent += 5

    

# Retrieve the "Top Level Domain Type" from the given link
def get_domain_type(link):
    global isBlog
    if "blog" in link:
        domain_type = urlsplit(link).hostname.split(".")[-1]
        isBlog = True
        return
    else :
        if link == "NoneType" or link == "":
            print("Error Reading Link")
            raise SystemExit
        else:
            domain_type = urlsplit(link).hostname.split(".")[-1]
            isBlog = False
            return domain_type
        

# Identify if the site type it's posted on gives or takes credibility away
def domain_percentage(top_level_domain):
    global informative_percent
    global isBlog
    top_levels = {"com" : 4, "net" : 2, "org" : 3, "gov" : 1, "edu" : 1, "co" : 4, "mil" : 1}
    if isBlog : 
        informative_percent += 5
    else:
        if top_level_domain not in top_levels:
            informative_percent += 5 # Default value
        else:
            informative_percent += top_levels[top_level_domain]  

def informative_link_context(link):
    global domain_name
    informative_link_edited = "https://mediabiasfactcheck.com/" + domain_name + "/"
    return informative_link_edited

def following_words(informative_link):
    global informative_percent
    response = requests.get(informative_link)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the text from the response
        html_content = response.text

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Desired phrases to search for
        desired_phrases = [
            "VERY HIGH",
            "HIGH",
            "MOSTLY FACTUAL",
            "MIXED",
            "LOW",
            "VERY LOW"
        ]

        # Find all span tags
        span_tags = soup.find_all('span')

        # Iterate through the span tags
        found_phrase = False
        # Iterate through the span tags
        for span in span_tags:
            # Check if the text inside the tag matches one of the desired phrases
            if span.text in desired_phrases:
                print(f"Found desired phrase: {span.text}")
                reporting = {"VERY HIGH" : 5, "HIGH" : 5, "MOSTLY FACTUAL" : 15, "MIXED" : 27, "LOW" : 45, "VERY LOW" : 45}
                informative_percent += reporting[span.text]
                found_phrase = True
                break

        if not found_phrase:
            informative_percent += 27

    else:
        informative_percent += 45
        return
        
# Anlyize the value of the misinformation percent
def safety_text(informative_percent):
    global safetyResult
    if(informative_percent > 50):
        if(informative_percent < 60):
            safetyResult = "likely"
        elif(informative_percent >= 60):
            safetyResult = "highly likely"
    else:
        if(informative_percent <= 35):
            safetyResult = "highly unlikely"
        elif(informative_percent < 50):
            safetyResult = "unlikely"
    


def getMisinformation(link):
    global informative_percent, domain_name, safetyResult, articles, top_level_domain, hostname, informative_link_for_input, domain_percentage, following_words, get_date_published, safety_text
    # Update the value depending on the link type .com / .net / .org, etc
    top_level_domain = get_domain_type(link)

    # Split the Url to give us the domain name
    hostname = urlsplit(link).hostname
    domain_name = ".".join(hostname.split(".")[-2:])
    domain_name = domain_name.split(".")[0]

    # Process the Likelyhood from the name of the link
    domain_percentage(top_level_domain)
    informative_link_for_input = informative_link_context(link)
    following_words(informative_link_for_input)
    get_date_published(link)

    # Analyze the reuslts
    safety_text(informative_percent)
    i, s, d = informative_percent, safetyResult, domain_name
    informative_percent, safetyResult, domain_name = 0, '', ''
    return i, s, d
# Print the result of the Misinformation Analysis
# print("The likelyhood of false information is ", informative_percent, "%, " + domain_name + " is " + safetyResult + " misinformation")