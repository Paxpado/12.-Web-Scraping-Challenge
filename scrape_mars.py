from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def init_browser():
    # Set up Splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # NASA Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    news = soup.find_all('div', class_='list_text')

    latest_title = []
    latest_body = []

    for n in news:
        title = n.find('div', class_='content_title')
        paragraph = n.find('div', class_='article_teaser_body')
        latest_title.append(title)
        latest_body.append(paragraph)

    latest_title1 = latest_title[0].text
    latest_body1 = latest_body[0].text  
    print(f'Latest Title: {latest_title1}')
    print(f'Latest Paragraph: {latest_body1}')

    # JPL Mars Space Featured Images
    url1 = "https://spaceimages-mars.com/"
    browser.visit(url1)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = url1 + \
        soup.find('img', class_='headerimage fade-in')['src']
    print(f'Featured Image URL: {featured_image_url}')

    # Mars Facts
    url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url)
    df = tables[1]
    html_table = df.to_html()
    html_table.replace('\n', '')
    print(html_table)

    # Mars Hemispheres
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemisphere_items = soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for item in hemisphere_items:
        try:
            # Hemisphere title
            title = item.find('div', class_='description').h3.text
            # hemisphere_title.append(title)
            # print(hemisphere_title)
            # Hemisphere Image URL
            thumbImage_url = item.find('a', class_='itemLink product-item')['href']
            # print(thumbImage_url)
            # Visit each thumbnail link
            browser.visit(url + thumbImage_url)
            time.sleep(3)
            html = browser.html
            soup = bs(html, 'html.parser')
            image_url = url + soup.find('img', class_='wide-image')['src']
            # Append
            hemisphere_image_urls.append({"Title": title, "img_url": image_url})

        except Exception as e:
            print(e)

    print(hemisphere_image_urls)

    browser.quit()

    print('Scraping Complete')

    mars_data = {
        "Latest_Title": latest_title,
        "Latest_Paragraph": latest_body,
        "Featured_Image_Url": featured_image_url,
        "Mars_Fact": html_table,
        "Hemisphere_Title_and_Images": hemisphere_image_urls}

    return mars_data
