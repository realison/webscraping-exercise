import  requests
import  csv
import  json
import  pandas as pd
from lxml import etree

# This is to get the permission of scraping 
def get_one_page(url):

    hd = {
         'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
    }
    # this is to find the exception
    try:
         response = requests.get(url, headers=hd)
         response.raise_for_status()
         response.encoding=response.apparent_encoding
         print('success')
    except:
        print('failure')
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    

#get the list of url

items_pages=[]
def parse_single_page(pages):
    pages=etree.HTML(pages)
    results_pages=pages.xpath("//div[@class='product-image js-product-plp-image tc']/a/@href")
    #list of pages
    
    for i in range(len(results_pages)):
        item={}
        item=results_pages[i]
        
        items_pages.append(item)
    return items_pages
    


#use the etree library to scrape data
def parse_item_xpath(html):
            price_items=[]
            brand_items=[]
            pname_items=[]
            review_items=[]
            
            for html in items_pages:
                        page_hd = {
                         #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
                        'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'}
               
                        response = requests.get(html, headers=page_hd)
                        try:
                             response.raise_for_status()
                             response.encoding=response.apparent_encoding
                             
                        except:
                            print('failure')
                        if response.status_code == 200:
                                text2 = response.content.decode('utf-8')
                                html_info= etree.HTML(text2)
                                price_result=html_info.xpath(
                                    "//span[@class='price-default']/span/text()")
                                
                                price_items.append(price_result)
                                
                                brand_result=html_info.xpath("//div[@class='pdp-product-brand f0']/a/text()")
                                brand_items.append(brand_result)
                                
                                pname_result=html_info.xpath("//span[@class='pdp-product-name__subtitle dn db-ns ttn f0']/text()")
                                pname_items.append(pname_result)
                                
                                review_result=html_info.xpath("//input[@id='ttReviewCount']/@value")
                                review_items.append(review_result)

                                
                                
            #print(price_items)
            df=pd.DataFrame({'price':price_items,'brand':brand_items,'name':pname_items,'review':review_items})
            print(df)
            df.to_csv('tanktops.csv',index=False)

        
              
        

def main():
        url = "https://www.aritzia.com/en/clothing/tshirts/tshirts-tank?lastViewed=157"
        page=get_one_page(url)
        items_pages=parse_single_page(page)
        print(items_pages)
        #items=parse_item_xpath(items_pages)
        parse_item_xpath(items_pages)
main()
