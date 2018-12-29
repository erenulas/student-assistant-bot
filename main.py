import time
from api_operations import (build_keyboard, get_last_update_id, get_updates, send_message)
from check_course import get_course_date
from check_product import get_product_price
from database import database
from urlshortener import shorten

db = database()

# handles responds to incoming commands and messages
def handle_updates(updates):
    for update in updates["result"]:
        #   gets the text and the chat id
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        sprt_index = text.find(" ")
        #   parses the text to identfiy the urls or names,stores, and commands
        if sprt_index != -1:
            command = text[0:sprt_index]
            url = text[sprt_index+1:]
            print("url:" + str(url.encode('utf-8')))
            num_of_args = text.count(" ")
            print("num: " + str(num_of_args))
        else:
            command = text
        #   response to start command
        if command == "/start":
            msg = "You can control this bot by sending the commands below.\n\n"
            msg = msg + "Commands:\n\n"
            msg = msg + "/addcourse www.url.com - adds a course page to database\n"
            msg = msg + "/addproduct www.url.com - adds a product to database\n"
            msg = msg + "/checkcourse - checks the announcements\n"
            msg = msg + "/checkproduct - checks a product's price\n"
            msg = msg + "/deletecourse - removes a course website from db\n"
            msg = msg + "/deleteproduct - removes a product from db\n"
            msg = msg + "/getcourseurl - returns the url of a course\n"
            msg = msg + "/getproducturl - returns the url of a product\n"
            msg = msg + "/productprice - returns the price of a product from db\n"
            msg = msg + "/courselastupdate - returns the date of the last update from db\n"
            msg = msg + "/getchatid - returns the chat id\n"
            msg = msg + "/updateprice newPrice - changes the price of a product\n"
            msg = msg + "/updatedate newDate- changes the date of last update of a course\n"
            send_message(msg, chat)
        #   functionality of addcourse command
        elif command == "/addcourse":
            product_or_course = 1
            #   gets the last modification date from website
            last_modified = get_course_date(url)
            if last_modified != -1:
                #   adds the course to db
                db.add_item(chat, url, "-1", "-1", product_or_course, last_modified)
                send_message("Course has been added", chat)
            else:
                send_message("Couldn't retrieve the last modified date", chat)
        #   functionality of addproduct command
        elif command == "/addproduct":
            product_or_course = 0
            #   gets name, store, and price of a product from website
            name, store, price = get_product_price(url)
            #   replaces spaces in the name of the product with comma
            name = name.replace(" ", ",")
            if price == -1:
                send_message("This website is not supported", chat)
            elif price == -2:
                send_message("Couldn't retrieve the price", chat)
            else:
                #   shortens the product url, and adds product to db
                #url = shorten(url)
                db.add_item(chat, url, store, name, product_or_course, price)
                send_message("Product has been added", chat)
        #   functionality of checkcourse command
        #   enters here when checkcourse command is sent without any other parameters
        elif command == "/checkcourse" and sprt_index == -1:
            #   gets all the courses from db
            items = db.get_items(chat, 1)
            #   builds the keyboard out of these courses
            keyboard = build_keyboard(items, command + " ", 1)
            #   shows the keyboard, and asks user to select one
            send_message("Select a course to check", chat, keyboard)
        #   enters here when checkcourse command is sent with a parameter
        elif command == "/checkcourse" and sprt_index != -1:
            #   gets the last modification date from db
            value_db = db.get_date(chat, url)
            value_db = "" + value_db[0]
            #   gets the last modification date from website
            value_current = get_course_date(url)
            #   if the values from db and website aren't equal, updates the value
            if value_db != value_current:
                db.update_value(value_current, chat, url)
                msg = "Website has been changed, press here to check -> " + url
            else:
                msg = "There aren't any new announcements made!"
            send_message(msg, chat)
        #   functionality of checkproduct command
        #   enters here when checkproduct is sent without any other parameters
        elif command == "/checkproduct" and sprt_index == -1:
            items = db.get_items(chat, 0)
            keyboard = build_keyboard(items, command + " ", 0)
            send_message("Select a product to check", chat, keyboard)
        #   enters here when checkproduct is sent with parameters
        elif command == "/checkproduct" and sprt_index != -1:
            #   parses the parameters part of the message to get the store and name of the product
            sprt_index2 = url.find(" ")
            store = url[0:sprt_index2]
            name = url[sprt_index2+1:]
            #   gets product's price from db
            value_db = db.get_price(chat, store, name)
            if len(value_db) > 0:
                value_db = "" + value_db[0]
            else:
                value_db = ""
            #   gets product's url
            
            url = db.get_url(chat, store, name)
            print(url)
            #   gets product's price from website
            _, _, value_current = get_product_price(url, store)
            #   if values from db and website are not equal, it updates the value with the current one
            if value_db is not None and value_db != value_current:
                db.update_value(value_current, chat, url)
                msg = "Previous price: " + value_db + "\nCurrent price: " + value_current
            else:
                msg = "It is still " + value_db
            send_message(msg, chat)
        #   functionality of deletecourse command
        elif command == "/deletecourse" and sprt_index == -1:
            items = db.get_items(chat, 1)
            keyboard = build_keyboard(items, command + " ", 1)
            send_message("Select a course to delete", chat, keyboard)
        elif command == "/deletecourse" and sprt_index != -1:
            db.delete_course(chat, url)
            send_message("Course is deleted", chat)
        #   functionality of deleteproduct command
        elif command == "/deleteproduct" and sprt_index == -1:
            items = db.get_items(chat, 0)
            keyboard = build_keyboard(items, command + " ", 0)
            send_message("Select a product to delete", chat, keyboard)
        elif command == "/deleteproduct" and sprt_index != -1:
            sprt_index2 = url.find(" ")
            store = url[0:sprt_index2]
            name = url[sprt_index2+1:]
            db.delete_product(chat, store, name)
            send_message("Product is deleted", chat)
        #   functionality of getcourseurl command
        elif command == "/getcourseurl" and sprt_index == -1:
            items = db.get_items(chat, 1)
            keyboard = build_keyboard(items, command + " ", 1)
            send_message("Select a url", chat, keyboard)
        elif command == "/getcourseurl" and sprt_index != -1:
            send_message(url, chat)
        #   functionality of getproducturl command
        elif command == "/getproducturl" and sprt_index == -1:
            items = db.get_items(chat, 0)
            keyboard = build_keyboard(items, command + " ", 0)
            send_message("Select a product", chat, keyboard)
        elif command == "/getproducturl" and sprt_index != -1:
            sprt_index2 = url.find(" ")
            store = url[0:sprt_index2]
            name = url[sprt_index2+1:]
            msg = db.get_url(chat, store, name)[0]
            send_message(msg, chat)
        #   functionality of productprice command
        elif command == "/productprice" and sprt_index == -1:
            items = db.get_items(chat, 0)
            keyboard = build_keyboard(items, command + " ", 0)
            send_message("Select a product", chat, keyboard)
        elif command == "/productprice" and sprt_index != -1:
            sprt_index2 = url.find(" ")
            store = url[0:sprt_index2]
            name = url[sprt_index2+1:]
            url = db.get_url(chat, store, name)[0]
            value = "" + db.get_price(chat, store, name)[0]
            msg = "Current price is " + value
            send_message(msg, chat)
        #   functionality of courselastupdate command
        elif command == "/courselastupdate" and sprt_index == -1:
            items = db.get_items(chat, 1)
            keyboard = build_keyboard(items, command + " ", 1)
            send_message("Select a course website", chat, keyboard)
        elif command == "/courselastupdate" and sprt_index != -1:
            value = "" + db.get_date(chat, url)[0]
            msg = "Last update is on " + value
            send_message(msg, chat)
        #   functionality of getchatid command
        elif command == "/getchatid" and sprt_index == -1:
            msg = "Chat id is " + str(chat)
            send_message(msg, chat)
        #   functionality of updateprice command
        #   enters here when updateprice command is sent with one parameter which is the new value
        elif command == "/updateprice" and sprt_index != -1 and num_of_args == 1:
            items = db.get_items(chat, 0)
            #   new value
            new_val = url
            #   puts new value to the texts in the keyboard
            keyboard = build_keyboard(items, command + " ", 0, new_val + " ")
            send_message("Select a product to update its price", chat, keyboard)
        elif command == "/updateprice" and sprt_index != -1:
            #   parses parameters part to get the store, name, and the new value
            sprt_index2 = url.find(" ")
            store = url[0:sprt_index2]
            name = url[sprt_index2+1:]
            sprt_index3 = name.find(" ")
            new_value = name[sprt_index3+1:]
            name = name[0:sprt_index3]
            #   gets the product url
            url = db.get_url(chat, store, name)[0]
            #   updates the price
            db.update_value(new_value, chat, url)
            send_message("Price has been updated", chat)
        #   functionality of updatedate command
        elif command == "/updatedate" and sprt_index != -1 and num_of_args == 1:
            items = db.get_items(chat, 1)
            new_val = url
            keyboard = build_keyboard(items, command + " ", 1, new_val + " ")
            send_message("Select a course page to update its last modified date", chat, keyboard)
        elif command == "/updatedate" and sprt_index != -1:
            sprt_index2 = url.find(" ")
            new_val = url[sprt_index2+1:]
            print(new_val)
            url = url[0:sprt_index2]
            print(url)
            db.update_value(new_val, chat, url)
            send_message("Date has been updated", chat)
        # if the command entered is not exist
        else:
            send_message("This command is not supported", chat)

def main():
    db.setup()
    last_update_id = None
    while True:
        #   gets the messages that is sent after the message with the last_update_id
        updates = get_updates(last_update_id)
        if  updates != -1 and len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
