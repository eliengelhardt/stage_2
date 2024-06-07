import requests
import time
import pandas as pd
import random
import os
import re
import concurrent.futures
import numpy as np
from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
import time
import random
import pandas as pd
from selenium.webdriver.common.by import By
import requests
from amazoncaptcha import AmazonCaptcha
from urllib.parse import quote_plus
import os
import openai
from ast import literal_eval
import google.generativeai as genai


def keyword_probability(keyword, title):
    similarity_ratio = fuzz.token_set_ratio(keyword.lower(), title.lower())
    return similarity_ratio
def getProxies():
    API_KEY = '8kbfgpt383t1p0681eimaw267xtoqg5n054eora7'
    res = requests.get("https://proxy.webshare.io/api/proxy/list/", headers={"Authorization": API_KEY})
    proxies = []
    for x in res.json()["results"]:
        proxy = f'{x["username"]}:{x["password"]}@{x["proxy_address"]}:{x["ports"]["http"]}'
        proxies.append(proxy)
    return proxies
def changeLocation(driver):
    try:
        driver.find_element(By.XPATH,'//*[@id="glow-ingress-block"]').click()   
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="GLUXZipUpdateInput"]').send_keys('77355')    
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="GLUXZipUpdate"]/span/input').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="a-autoid-3-announce"]').click()
        
        try:
            driver.find_element(By.XPATH,'//*[@id="GLUXConfirmClose"]').click()
        except:
            pass
            
        return True
    except:
        return False
def checkCaptcha(driver):
    try:
        url = driver.find_element(By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img').get_attribute('src')
        solveCaptcha(url,driver)
        return True
    except:
        return False
def solveCaptcha(url,driver):
    response = requests.get(url)
    if response.status_code == 200:
        with open("captcha.jpg", "wb") as f:
            f.write(response.content)
        print("Image saved as captcha.jpg")
        captcha = AmazonCaptcha('captcha.jpg')
        solution = captcha.solve()
        driver.find_element(By.XPATH,'//*[@id="captchacharacters"]').send_keys(solution)
        time.sleep(2)
        driver.find_element(By.XPATH,'/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button').click()
        return solution
    else:
        print("Failed to download image")
def extractDecimal(text):
    pattern = r'\$?(\d+(\.\d+)?)'
    matches = re.findall(pattern, text)

    if matches:
        tempPrice = float(matches[0][0])
        return tempPrice
    else:
        return 0

def generateSearchTerms(keyword,title,bulletPoints):
    gptInput = {'title':title,'keyword':keyword,'bulletPoints':bulletPoints}
    
    
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0125",
      messages=[
        {"role": "system", "content": f"""Given a title, base word, and bullet points,
        I want you to generate 2 search term that will help me find products exactly matching the provided details. I should be able to find the exact products with same model , unit , size and quantity. Generate search terms accordingly 
        The search terms should include the keyword and be specific enough to retrieve precise matches. Please provide the search terms as a Python list.
        """},
          {"role":"user","content":str(gptInput)}
      ]
    )

    return completion.choices[0].message['content']
def getSearchResults(searchTerm,cookies_string,proxies,referencePrice):
    searchTerm = quote_plus(searchTerm)
    
    dfs = []
    headers = {
          'authority': 'www.amazon.com',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
          'cache-control': 'max-age=0',
          'cookie': cookies_string,
          'device-memory': '8',
          'downlink': '10',
          'dpr': '1.297999942302704',
          'ect': '4g',
          'rtt': '50',
          'sec-ch-device-memory': '8',
          'sec-ch-dpr': '1.297999942302704',
          'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-ch-ua-platform-version': '"15.0.0"',
          'sec-ch-viewport-width': '1480',
          'sec-fetch-dest': 'document',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-site': 'none',
          'sec-fetch-user': '?1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
          'viewport-width': '1480'
        }
    driver.get(f'https://www.amazon.com/s?k={searchTerm}&rh=p_36%3A-{referencePrice}')
#     time.sleep(2)
#     try:
#         driver.find_element(By.XPATH,'//*[@id="a-autoid-0"]/span').click()
#         time.sleep(1)
#         driver.find_element(By.XPATH,'//*[@id="s-result-sort-select_1"]').click()
#         print("Applied filter successfully")
#     except:
#         print("Error")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    urls = []
    urls.append('')
    for i in soup.find_all(class_='s-pagination-item s-pagination-button'):
        urls.append('https://www.amazon.com'+i['href'])
    for page in urls[:1]:
        if page =='':
            pass
        else:
            driver.get(page)
            time.sleep(4)
#         soup = BeautifulSoup(driver.page_source,'html.parser')

#         proxy = random.choice(proxies)|
#         os.environ["http_proxy"] = 'http://'+proxy
#         os.environ["https_proxy"] = 'http://'+proxy
#         if page==1:
#             response = requests.get(f'https://www.amazon.com/s?k={searchTerm}',headers=headers)
#         else:
#             response = requests.get(f'https://www.amazon.com/s?k={searchTerm}&page={page}',headers=headers)
#         print(response)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        elements = soup.find_all("div", attrs={"data-asin": True})
        itemName = []
        asin = []
        amazonPrime = []
        deliveryByAmazon = []
        price = []
        for element in elements:
            if element['data-asin'] != '':
                asin.append(element['data-asin'])
            else:
                continue
            try:
                itemName.append(element.find(class_='a-size-medium a-color-base a-text-normal').text)
            except:
                try:
                    itemName.append(element.find(class_='s-link-style').text)
                except:
                    itemName.append('')
            try:
                tempPrice = element.find(class_='a-offscreen').text
                tempPrice = extractDecimal(tempPrice)
                price.append(tempPrice)
            except:
                price.append(0)


            try:
                if element.find(class_='a-icon a-icon-prime a-icon-medium')['aria-label'] =='Amazon Prime':
                    amazonPrimeFlag = True
                else:
                    amazonPrimeFlag = False
            except:
                amazonPrimeFlag = False
            amazonPrime.append(amazonPrimeFlag)
            belowText = []
            for tag in element.find_all('span',class_='a-color-base'):
                try:
                    belowText.append(tag.text)
                except:
                    belowText.append('')
            belowText = ','.join(belowText)
            if 'shipped by Amazon' in belowText:
                shippedByAmazonFlag = True
            else:
                shippedByAmazonFlag = False
            deliveryByAmazon.append(shippedByAmazonFlag)
        df = pd.DataFrame({
        'Item Name': itemName,
        'ASIN': asin,
        'Amazon Prime': amazonPrime,
        'Delivery by Amazon': deliveryByAmazon,
        'Price': price
        })
        dfs.append(df)
    data = pd.concat(dfs)
    return data
def getProductDetails(asin,cookies_string,proxy):
    time.sleep(1)
    if proxy =='':
        pass
    else:
        pass
#         os.environ["http_proxy"] = 'http://'+proxy
#         os.environ["https_proxy"] = 'http://'+proxy
    
    headers = {
          'authority': 'www.amazon.com',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
          'cache-control': 'max-age=0',
          'cookie': cookies_string,
          'device-memory': '8',
          'downlink': '10',
          'dpr': '1.297999942302704',
          'ect': '4g',
          'rtt': '50',
          'sec-ch-device-memory': '8',
          'sec-ch-dpr': '1.297999942302704',
          'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-ch-ua-platform-version': '"15.0.0"',
          'sec-ch-viewport-width': '1480',
          'sec-fetch-dest': 'document',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-site': 'none',
          'sec-fetch-user': '?1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
          'viewport-width': '1480'
        }
    url = f'https://www.amazon.com/dp/{asin}'
    
    response = requests.get(url,headers=headers)
    print(response)
    jsonData = {}
    soup = BeautifulSoup(response.text,'html.parser')
    jsonData['ASIN'] = asin
    
    try:
        jsonData['TITLE'] = soup.find(id = 'productTitle').text.strip(' ')
    except:
        jsonData['TITLE'] = ''
    
    
    
    try:
        tempPrice = soup.find(class_='a-section a-spacing-none aok-align-center aok-relative').find(class_='aok-offscreen').text
        tempPrice = extractDecimal(tempPrice)
        jsonData['PRICE'] = tempPrice
    except:
        jsonData['PRICE'] = ''
    try:
        bulletPoints = []
        for li in soup.find(class_='a-unordered-list a-vertical a-spacing-mini').find_all('li'):
            bulletPoints.append(li.text.strip())
        jsonData['BULLETPOINTS'] = bulletPoints
    except:
        jsonData['BULLETPOINTS'] = []
    try:
        jsonData['EXTRADATA'] = soup.find(class_='a-normal a-spacing-micro').text
    except:
        jsonData['EXTRADATA'] = ''
        
    return jsonData

proxies = getProxies()

time.sleep(5)

# Initializing Driver

# ip = random.choice(proxies)
# ip = proxies[0]
directory = 'Scraped Products'

if not os.path.exists(directory):
    os.makedirs(directory)
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument("disable-infobars")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')
# options.se
# ip = random.choice(proxies)
# wireOptions = {
#         'proxy':{
#             'http': f'http://{ip}',
#             'https': f'https://{ip}',
#             'no_proxy': "http://localhost,127.0.0.1"

#         }
#     }
driver = webdriver.Chrome(options=options)
driver.get('https://www.amazon.com/')

time.sleep(5)

# Solving Captcha
checkCaptcha(driver)

time.sleep(5)

# Changing Location
changeLocation(driver)

time.sleep(5)

# Getting Cookies for further requests
cookies = driver.get_cookies()
cookies_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

time.sleep(5)

# Scraping Data
inputDf = pd.read_excel('inputSheet.xlsx')
# proxies = []
dataFrames = []
for index,row in inputDf.iterrows():
    print("Getting Reference Product")
    referenceAsin = row['referenceAsin']
    keyword = row['keyword']
    
    referenceProduct = getProductDetails(referenceAsin,cookies_string,random.choice(proxies))  
    searchTerms = generateSearchTerms(keyword,referenceProduct['TITLE'],referenceProduct['BULLETPOINTS'])
    try:
        try:
            searchTerms = literal_eval(searchTerms)
        except:
            searchTerms = generateSearchTerms(keyword,referenceProduct['TITLE'],referenceProduct['BULLETPOINTS'])
            searchTerms = literal_eval(searchTerms)
    except:
        start_idx = searchTerms.find('[')
        end_idx = searchTerms.find(']') + 1
        searchTerms = searchTerms[start_idx:end_idx]
        searchTerms = literal_eval(searchTerms)
    referencePrice = referenceProduct['PRICE']*100
    referencePrice = int(referencePrice)
    dfs = []
    print("Getting Search Results")
    print(searchTerms)
    searchTerms.append(referenceProduct['TITLE'])
    for serachTerm in searchTerms:
        print(serachTerm)
        frame = getSearchResults(serachTerm,cookies_string,proxies,referencePrice)
        dfs.append(frame)
    df = pd.concat(dfs)
    df = df.drop_duplicates(subset=['ASIN'])
    df = df[df['Price']!=0]
    df = df[df['Price']<referenceProduct['PRICE']]
    df = df[df['Item Name']!='Leave ad feedback ']
    df = df[(df['Amazon Prime'] == True) | (df['Delivery by Amazon'] == True)]
    # keywordProbability = []
    # for title in list(df['Item Name']):
    #     keywordProbability.append(keyword_probability(keyword, title))
    asins = list(df['ASIN'])
    
    print("Total results found :",len(asins))
    jsonData = []
    for asin in asins:
        print(asin)
        try:
            details = getProductDetails(asin,cookies_string,random.choice(proxies))
        except:
            time.sleep(2)
            details = getProductDetails(asin,cookies_string,random.choice(proxies))
            
        jsonData.append(details)
    if jsonData ==[]:
        continue
    furtherDetails = pd.DataFrame(jsonData)
    df['Bullet Points'] = list(furtherDetails['BULLETPOINTS'])
    df['Extra Attributes'] = list(furtherDetails['EXTRADATA'])
    df = df.sort_values(by='Price')
    df['GENERATED SEARCH TERMS'] = str(searchTerms)
    keyword = keyword.replace("/",'')
    
    df.to_excel(f'Scraped Products/{referenceAsin}-{keyword}.xlsx',index=False)
    dataFrames.append(df)
#     break

time.sleep(5)

asins = list(inputDf['referenceAsin'])
allProducts = []
referenceProducts = []
for frame,asin in zip(dataFrames,asins):
    proxy = random.choice(proxies)
    try:
        referenceProduct = getProductDetails(asin,cookies_string,proxy)
    except:
        time.sleep(3)
        referenceProduct = getProductDetails(asin,cookies_string,proxy)
        
    referenceProducts.append(referenceProduct)
    products = []
    for i,row in frame.iterrows():
        d = {}
        d['title'] = row['Item Name']
        d['bulletPoints'] = row['Bullet Points']
        d['price'] = row['Price']    
        d['asin'] = row['ASIN']
        products.append(d)
    allProducts.append(products)

time.sleep(5)

# Initializing Gemini AI API
genai.configure(api_key="AIzaSyAtxMItZfoimEZpEd-Vgjp5v0kusb71UvE")
# genai.configure(api_key="AIzaSyBjSG2mFaCrrDU9cyr_dJ_S06fNLc9pq14")
safe = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

time.sleep(5)

# Getting Quantities
categories = list(inputDf['keyword'])
quantityDataframes = []
limit = 100
model = genai.GenerativeModel('gemini-1.0-pro-latest')
for searchResults,referenceProduct,category in zip(allProducts,referenceProducts,categories):
    print(category)
    print("Products :",len(searchResults))
    df = pd.DataFrame(searchResults[:limit])
    referenceProduct = referenceProduct
    quantity = []
    for product in searchResults[:limit]:
        try:
            response = model.generate_content(f"""
            I am providing some product data like title, description and bullet points, You have to identify the quantity of the product, Like how
            much it is , 1 ,2 etc. Make sure you don't take size of the product as quantity, It should be always number of items/pieces in that listings. I want you to only return a number quantity, Thats it. 
            PRODUCTS :{product}""",safety_settings=safe)
            time.sleep(4)
            quantity.append(response.text)
        except:
            time.sleep(20)
            response = model.generate_content(f"""
            I am providing some product data like title, description and bullet points, You have to identify the quantity of the product, Like how
            much it is , 1 ,2 etc. Make sure you don't take size of the product as quantity, It should be always number of items/pieces in that listings. I want you to only return a number quantity, Thats it. 
            PRODUCTS :{product}""",safety_settings=safe)
            time.sleep(4)
            quantity.append(response.text)

    time.sleep(5)
    df['Quantity'] = quantity
    quantityDataframes.append(df)
#     break

time.sleep(5)

# Filtering Quantity Based on Reference Product Quantity
filteredDataframe = []
model = genai.GenerativeModel('gemini-1.0-pro-latest')
for frame,referenceProduct in zip(quantityDataframes,referenceProducts):
    print(frame.shape)
    time.sleep(4)
    try:
        response = model.generate_content(f"""
            I am providing some product data like title, description and bullet points, You have to identify the quantity of the product, Like how
            much it is , 1 ,2 etc. Make sure you don't take size of the product as quantity, It should be always number of items/pieces in that listings. I want you to only return a number quantity, Thats it.
            if you cannot identify the quantity, then just return 1.
            PRODUCTS :{referenceProduct}""",safety_settings=safe)
    except:
        time.sleep(20)
        response = model.generate_content(f"""
            I am providing some product data like title, description and bullet points, You have to identify the quantity of the product, Like how
            much it is , 1 ,2 etc. Make sure you don't take size of the product as quantity, It should be always number of items/pieces in that listings. I want you to only return a number quantity, Thats it.
            if you cannot identify the quantity, then just return 1.
            PRODUCTS :{referenceProduct}""",safety_settings=safe)

    referenceProductQuantity = response.text
    newQuantity = []
    for quantity in frame['Quantity']:
        try:
            newQuantity.append(int(quantity))
        except:
            newQuantity.append(0)
    frame['newQuantity'] = newQuantity
    frame = frame[frame['newQuantity']==int(referenceProductQuantity)]
    filteredDataframe.append(frame)
#     break

time.sleep(5)

# Final Logic for finding interchangeable 
results = []
model = genai.GenerativeModel('gemini-1.5-pro-latest')
for frame,referenceProduct,category in zip(filteredDataframe,referenceProducts,categories):
    print(category)
    frameJson = []
    for i,row in frame.iterrows():
        temp = {}
        temp['title'] = row['title']
        temp['bulletPoints'] = row['bulletPoints']
        temp['asin'] = row['asin']
        temp['newQuantity']=row['newQuantity']
        frameJson.append(temp)
    products = str(frameJson)        
        
    response = model.generate_content(f"""
        I am providing a list of PRODUCTS and a REFERENCE PRODUCT , I want you to give me all the asin of products which are
        similar to the REFERENCE. Note that the model , unit , specifications and size should be strictly same as reference product.
        I am also providing the keyword, The product should be similar to reference product and should have keyword in it.
        Return a list of asins which you find similar or interchangeablebuy. The list should be a python list.I should only have
        product asins and no other details. The list should have only 5 or less asins , not more than that.

        KEYWORD :{category}
        REFERENCEE PRODUCTS {referenceProduct}
        PRODUCTS :{products}""",safety_settings=safe)
    time.sleep(60)
    print(response.text)
    results.append(response.text)
#     results.append(responseText)
#     time.sleep(30)
#     break

time.sleep(5)

# Generating a output file 
pd.DataFrame({'Category':categories,'Results':results}).to_excel('SAMPLE.xlsx',index=False)