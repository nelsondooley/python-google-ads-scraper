import pandas as pd
import time
from requests_html import HTMLSession
from selenium import webdriver

session = HTMLSession()

ad_list = [] #empty list to store ad details

df_keywords = pd.read_csv('top-keywords_test.csv', index_col =None, header=0 ) #getting top ad keywords out of a CSV

for keyword in df_keywords.Keyword:
    #loop thru each of the top 20 most expensive adwords keywords
    print(keyword)
    r = session.get('https://google.com/search?q='+keyword)

    #get the 4 ads at the top
    ads = r.html.find('.ads-ad')

    for ad in ads:
        ad_link = ad.find('.V0MxL', first=True).absolute_links #link to landing page
        ad_link = next(iter(ad_link)) #need this since the result from above is set
        ad_headline = ad.find('h3.sA5rQ', first=True).text #headline of the ad
        ad_copy = ad.find('.ads-creative', first=True).text #ad copy
        ad_list.append([keyword, ad_link, ad_headline, ad_copy]) #append data row to list

df_ads = pd.DataFrame(ad_list, columns = ['keyword', 'ad_link', 'ad_headline', 'ad_copy'])

#timestamp so we dont overwrite old CSVs
ts = time.time()
#write out to CSV for reference
df_ads.to_csv('top-ads-'+str(ts)+'.csv')

#Selenium loop thru dataframe to save PNGs into "screenshots" folder
for index, row in df_ads.iterrows():
    print('Index: ' + str(index) + ', Ad Link: ' + row['ad_link'])
    browser = webdriver.Firefox()
    browser.get(row['ad_link'])
    browser.save_screenshot('screenshots/'+str(index)+'.png')
    browser.quit()