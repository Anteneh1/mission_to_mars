# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import time
import pandas as pd


def init_browser():
    # @NOTE: Replacing the path with the actual path to the chromedriver
    

    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return  Browser('chrome',**executable_path, headless= False) 

def scrape():
    browser = init_browser()
    mars_info = { }
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('ul', class_= 'item_list')

    article = results.find('li', class_ ='slide')
    
    titles_header = article.find('div', class_ = 'content_title').text
        
    body_par = article.find('div', class_= 'article_teaser_body').text
    
    #mars_info.header = titles_header
   # mars_info.paragraph = body_par
    mars_info['header'] = titles_header
    mars_info['paragraph'] = body_par   




    # visit the  website and scrape the  image 
    #
    #
    browser = init_browser()

    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image_url)
    time.sleep(1)


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    try:
        expand = browser.find_by_css('a.fancybox-expand')
        expand.click()
        time.sleep(1)

        jpl_html = browser.html
        jpl_soup = bs(jpl_html, 'html.parser')

        img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
        image_path = f'https://www.jpl.nasa.gov{img_relative}'
        mars_info['image'] = image_path

    #except ElementNotVisibleException 
    except NameError & ElementNotVisibleException:
        image_path = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22076_hires.jpg'
        mars_info['image'] = image_path
    
    #browser.click_link_by_partial_text('more info')
    #time.sleep(1)

    #html_object = browser.html

    #soup = bs(html_object, 'html.parser')

    #results = soup.find( class_= 'lede')

    #result= results.find('a')
    #href = result['href']

    #article = soup.find( property ="og:image")
    #href = article['content']  
    #mars_info['image_url'] = href




    # visit the mars weather report twitter and scrape the latest tweet
    #
    #
    browser = init_browser()

    tweet_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(tweet_url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    mars = soup.find_all('div', class_='content')[20]

    weather = mars.find('p', class_="TweetTextSize").text
    mars_info['weather'] = weather


       
    # scrap for facts
    #
    #

    browser = init_browser()

    fact_url = 'http://space-facts.com/mars/'
    browser.visit(fact_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    #fact_table = soup.find_all('table', class_='tablepress tablepress-id-mars')


    header = []
    value = []
    descriptions = soup.find_all("td",class_='column-1')
    for description in descriptions:
        describe=description.text.strip()
        header.append(describe)
    figures = soup.find_all('td', class_='column-2')
    for figure in figures:
        values = figure.text.strip()
        value.append(values)
    
    
    mars_facts = pd.DataFrame({
        "Header":header,
        "Value":value
        })
    mars_facts = mars_facts.to_html(header=False, index=False)
    mars_facts_html = mars_facts.strip()
    mars_info['facts'] = mars_facts_html

    

    # mars hemisphere
    #
    #



    browser = init_browser()

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_address_list = []
    titles_name = []
    
    

    for x in range(1,9,2):

        
        browser.visit(hemisphere_url)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')
        links = soup.find_all('a', class_='itemLink product-item')
    
    
        title_list = links[x].text.strip('Hemisphere Enhanced')
    
        titles_name.append(title_list)
    
    
        #
        element_link = browser.find_by_css('a.product-item') 
                      
        element_link[x].click()
    
        browser.find_link_by_text('Sample').first.click()
        time.sleep(10)
        browser.windows.current = browser.windows[-1]
    
        img_url = browser.html
    
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
    
        url_img_soup = bs(img_url,'lxml')
        url_address = url_img_soup.find('img')['src']
    
        url_address_list.append(url_address)
        
        
    #
    mars_info['hemisphere'] =titles_name
    mars_info['link'] = url_address_list
    

   
    
    browser.quit()
    return mars_info
    
            