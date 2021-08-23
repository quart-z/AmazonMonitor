# Updated as of 8/21/21
# Grabs OID from amazon, needed for monitoring / botting
# Made by quart-z on github

import requests
import lxml
from bs4 import BeautifulSoup


headersAmazon = {
    'authority': 'www.amazon.com',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
}

class AmazonMonitor():
    def __init__(self):
        self.s = requests.Session() # first variable used in classes
        self.responseSoup = "" # current responseSoup

    def getResponse(self, SKU): # Gets a basic response from a webpage, and parses accordingly to lxml
        response = self.s.get(f"https://www.amazon.com/gp/aws/cart/add.html?ASIN.1={SKU}&Quantity.1=1&AssociateTag=FC", headers = headersAmazon)
        return BeautifulSoup(response.text, "lxml") # parses text from response into lxml

    def getPrice(self, SKU):
        try:
            responseSoup = self.getResponse(SKU)

            priceFind = responseSoup.find("td", {"class": "price item-row"}).text.strip()
            return priceFind

        except Exception as e:
            print("Exception occured: " + e)

    def getOfferID(self, SKU):
        try:
            responseSoup = self.getResponse(SKU)

            offerID = responseSoup.find("input", {"name": "OfferListingId.1"})["value"]
            return offerID

        except Exception as e:
            print("Exception occured: " + e)


#----- MAIN -----#



sku = input("Paste Amazon sku to get the current best offer: \n") # Sku is in form such as example: B084LMWSJG

OID = AmazonMonitor().getOfferID(sku) # calls main function
price = AmazonMonitor().getPrice(sku) # calls main function


print (f"\nBest offer found!\n\nOID: {OID}\nPrice: {price}\n\nMake sure to double check price with amazon's price, to make sure you found the correct offerID!")









