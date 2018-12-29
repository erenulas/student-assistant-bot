import requests
from bs4 import BeautifulSoup

def get_product_price(url, store=""):
    try:
        #   makes a request to the website, and puts the response into response.
        response = requests.get(url)
        #   puts the html of the webpage into soup
        soup = BeautifulSoup(response.content, 'html.parser')
        #   checks if the url belongs to teknosa
        if url.find("teknosa") != -1 or store == "teknosa":
            #   finds the 'new-price' class in code and gets its text as the price
            price = soup.find(class_="new-price").get_text()
            #   since this block executes if the url belongs to teknosa, store is equal to teknosa
            store = "teknosa"
            #   finds the 'product-name' class in html and gets its text as the name of the product
            name = soup.find(class_="product-name").get_text()
            return name, store, price
        #   checks if the url belongs to hepsiburada
        elif url.find("hepsiburada") != -1 or store == "hepsiburada":
            #   gets the price from html of webpage
            price = ""
            temp = soup.find('span', class_="price")
            if temp is not None:
                price = price + temp.select("span")[0].get_text() + ","
                price = price + temp.select("span")[1].get_text() + " "
                currency = soup.find('span', class_="turkishLira").get_text()
                price = price + currency
            
            store = "hepsiburada"
            #   gets the name of the product
            name = soup.find(class_="product-name")
            if name is not None:
                name = name.get_text()
            else:
                name = ""
            return name, store, price
        #   checks if the url belongs to gittigidiyor
        elif url.find("gittigidiyor") != -1 or store == "gittigidiyor":
            #   gets the price of the product from html of website
            price = soup.find(class_="product-price-info-con")
            price = price.select("strong")[0].get_text()
            price = price + " TL"

            store = "gittigidiyor"
            #   gets the product name
            name = soup.find('span', class_="title").get_text()
            return name, store, price
        #   checks if the url belongs to n11
        elif url.find("n11") != -1 or store == "n11":
            #   gets the price
            price = soup.find(class_="newPrice")
            price = price.select("ins")[0].get_text()

            store = "n11"
            #   gets the name
            name = soup.find(class_="proName").get_text()
            return name, store, price
        else:
            # if the url isn't one of teknosa's, hepsiburada's, gittigidiyor's or n11's, then returns -1
            return "-1", "-1", "-1"
    except requests.exceptions.RequestException as e:
        #   if an exception occurs when connecting to page, executes here
        print(e)
        return "-2", "-2", "-2"
