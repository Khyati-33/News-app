from flask import Flask, render_template, request
from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pytz import timezone

app = Flask(__name__)
NEWS_API_KEY = 'aee7a2484e074e4b903dd3714f384f2e'
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        if query:
            articles = search_articles(query)
        else:
            # Display news from Times of India on the homepage
            articles = get_toi_news()
    else:
        # Display news from Times of India on the homepage
        articles = get_toi_news()

    # Get live date and time in the 'Asia/Kolkata' timezone
    india_timezone = timezone('Asia/Kolkata')
    live_date_time = datetime.now(india_timezone).strftime('%d %B %Y, %I:%M %p')

    # Fetch latest tech news from The Verge
    tech_news = get_verge_tech_news()
    today_news=get_today_news()

    return render_template('index.html', articles=articles, live_date_time=live_date_time, tech_news=tech_news)

def get_today_news():
    toi_url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(toi_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    today_news = []

    # Extract headlines and links from Times of India homepage
    headlines = soup.find_all('span', class_='w_tle')
    links = soup.find_all('a', class_='w_img')

    # Get today's date in the format used on the website
    today_date = datetime.now().strftime('%d %b %Y').lower()

    for headline, link in zip(headlines, links):
        news_title = headline.get_text(strip=True)
        news_link = link['href']

        # Extract the date from the link (assuming it's in the format 'yyyy/mm/dd')
        link_parts = news_link.split('/')
        news_date = f"{link_parts[3]} {link_parts[4]} {link_parts[5]}".lower()

        # If the news is from today, add it to the list
        if today_date == news_date:
            today_news.append({'title': news_title, 'link': news_link, 'time': ''})

    return today_news

def search_articles(query):
    all_articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)
    return all_articles['articles']

def get_toi_news():
    toi_url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(toi_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    toi_news = []

    # Extract headlines and links from Times of India homepage
    headlines = soup.find_all('span', class_='w_tle')
    links = soup.find_all('a', class_='w_img')

    for headline, link in zip(headlines, links):
        news_title = headline.get_text(strip=True)
        news_link = link['href']
        toi_news.append({'title': news_title, 'link': news_link})

    return toi_news

def get_verge_tech_news():
    url = 'https://www.theverge.com/tech'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tech_news = []

    # Extract tech news headlines, links, and publication date
    articles = soup.find_all('div', class_='c-entry-box--compact')
    for article in articles:
        news_title = article.find('h2', class_='c-entry-box--compact__title').get_text(strip=True)
        news_link = article.find('a', class_='c-entry-box--compact__link')['href']
        
        # Extracting the publication time
        news_time = article.find('time')['data-chorus-optimize-field']
        
        tech_news.append({'title': news_title, 'link': news_link, 'time': news_time})

    return tech_news

if __name__ == '__main__':
    app.run(debug=True)

    
