# Bot that gets amazon info when a product is in stock, and sends to a given discord webhook
# Only fields you need to change are the discord webhook in AmazonInfo.()sendAmazonWebhook(), and skuList at the bottom of the program


import requests
import lxml
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed # best working module for webhooks in my experience
import time # sleep() function for loop
from datetime import datetime # gets current date for webhook
import numpy as np
import random


headersAmazon = { 
    'authority': 'www.amazon.com',
    'cache-control': 'max-age=0',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9',
    }


class AmazonInfo():
    def __init__(self):
        self.s = requests.Session() # first variable used in classes
        self.responseSoup = "" # current responseSoup

    def sendAmazonWebhook(self, title, image, price, SKU):
        # Input whatever webhook you'd like in between the "" in the DiscordWebhook function
        webhook = DiscordWebhook("")
        
        # Two pictures being used in the webhook, you can change these or add more  
        storeLogo = "https://cdn0.iconfinder.com/data/icons/most-usable-logos/120/Amazon-512.png"
        serverLogo = "https://testcreative.co.uk/wp-content/uploads/2018/08/logo.png"

        # All fields used in the webhook, can change/ add more or less
        embed = DiscordEmbed(title = (title), url = f"https://www.amazon.com/gp/offer-listing/{SKU}?ref=flipcent?ie=UTF8&m=ATVPDKIKX0DER&language=en_US", description = "Amazon Stock Live", color = 0xFF9900)
        embed.set_author(name = "Amazon Monitor", icon_url = storeLogo)
        embed.set_footer(text = "Test", icon_url = serverLogo)
        embed.set_timestamp()
        embed.set_thumbnail(url = (image))
        embed.add_embed_field(name = "Add To Cart", value = f"[Add To Cart](https://www.amazon.com/gp/aws/cart/add.html?ASIN.1={SKU}&Quantity.1=1&AssociateTag=quart-z)")
        embed.add_embed_field(name = "Price", value =(price))
        embed.add_embed_field(name ="SKU", value = (SKU))

        # Final execution
        try:
            webhook.add_embed(embed)
            webhook.execute()
        except:
            print("No webhook specifed! Input a webhook on line 39 of this program!") # If user doesn't enter a webhook URL


    def getTitle(self, SKU):
        titleFind = self.responseSoup.find("title", {"dir": "ltr"}) # finds title in soup
        titleStripped = titleFind.text.strip() # finds response
        splitTitle = titleStripped.split('Choices: ')[1] # splits title, and prints text after 'Choices: ', which is list value [1]

        return splitTitle # returns if sold, or in stock


    def getImage(self, SKU):
        imageFind = self.responseSoup.find("img", {"alt": "Return to product information"}) # finds image in soup
        imageURL = imageFind["src"] # finds imageURL in soup further, anything after "src"

        return imageURL # returns if sold, or in stock


    def getPrice(self, SKU):
        priceFind = self.responseSoup.find("span", {"class": "a-size-large a-color-price olpOfferPrice a-text-bold"}) # finds price in soup
        priceFindResponse = priceFind.text.strip() # finds response

        return priceFindResponse # returns if sold, or in stock

    def getResponse(self, SKU): # Gets a basic response from a webpage, and parses accordingly to lxml
        response = self.s.get(f"https://www.amazon.com/gp/offer-listing/{SKU}?ie=UTF8&m=ATVPDKIKX0DER&language=en_US", headers = headersAmazon)
        responseSoup = BeautifulSoup(response.text, "lxml") # parses text from response

        return responseSoup


    def getProductStatus(self, SKU): # checks if amazon is selling product or not
        self.responseSoup = self.getResponse(SKU) # Gets a response from the website and stores in __init__ variable
        atcFind = self.responseSoup.find("div", {"class": "a-section a-padding-small"}) # finds headline of atc button

        atcFindResponse = atcFind.text.strip() # finds response
        return atcFindResponse # returns if sold, or in stock


    def monitorProduct(self, SKU): # monitors if amazon is the seller of the produce
        currentVersion = self.getProductStatus(SKU) # gets if product is sold out or not

        if (currentVersion == "Currently, there are no sellers that can deliver this item to your location."): # if this is the case, the product is sold out
            currentVersion = "Sold" # print sold
        else:
            currentVersion = "Available" # print available

        return currentVersion # returns status


    def detectChanges(self, skuList):
        print("Starting " + str(self.__class__.__name__)) 

        currentVersionList = skuList[:]
        for i in range(len(skuList)):
            currentVersionList[i] = self.monitorProduct(skuList[i]) # calls function with SKU 'i'

        for i in range(len(skuList)):
            if (currentVersionList[i] == "Available"): # if changes to Available, means it is in stock
                print("Product is in stock!")
                title = self.getTitle(skuList[i]) # gets title and stores
                image = self.getImage(skuList[i]) # gets image and stores
                price = self.getPrice(skuList[i]) # gets price and stores
                self.sendAmazonWebhook(title, image, price, skuList[i]) # sends webhook
            else:
                print("Product is sold out!")

        print ("End of current monitor, time: " + str(datetime.now().strftime("%H:%M:%S")) + "\n") # Prints time






# Input SKU of product on amazon here, sample given.
skuList = ["B08CYQ7VJ4"] 
AmazonInfo().detectChanges(skuList) # calls main function


