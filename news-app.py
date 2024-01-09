from flask import Flask, render_template, request
from newsapi import NewsApiClient
from datetime import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup

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

    return render_template('index.html', articles=articles, live_date_time=live_date_time, tech_news=tech_news)

def search_articles(query):
    all_articles = newsapi.get_everything(q=query, language='en', sort_by='relevancy', page_size=5)
    return all_articles['articles']


def get_toi_news():
    toi_url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(toi_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    today_news = []

    # Extract headlines, links, and publication time from Times of India homepage
    headlines = soup.find_all('span', class_='w_tle')
    links = soup.find_all('a', class_='w_img')
    times = soup.find_all('span', class_='update-time')

    for headline, link, time in zip(headlines, links, times):
        news_title = headline.get_text(strip=True)
        news_link = link['href']
        news_time = time.get_text(strip=True)

        # Parse the publication time and check if it's today's news
        news_datetime = datetime.strptime(news_time, '%d %b, %Y, %H:%M %p')
        today_date = datetime.now().date()
        if news_datetime.date() == today_date:
            today_news.append({'title': news_title, 'link': news_link, 'time': news_time})

    return today_news

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
        news_time = article.find('time')['data-chorus-optimize-field']="datehedg" # Extracting the publication time
        tech_news.append({'title': news_title, 'link': news_link, 'time': news_time})

    return tech_news

if __name__ == '__main__':
    app.run(debug=True)