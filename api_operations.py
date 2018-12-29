import json
import requests
import urllib

#   token to access api
TOKEN = <TOKEN>
#   base url for Telegram api
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#   gets the content from the url
def get_url(url):
    try:
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
    except requests.exceptions.RequestException as e:
        print(e)
        return -1

#   converts json content to dictionary
def get_json_from_url(url):
    content = get_url(url)
    if content != -1:
        js = json.loads(content)
        return js
    else:
        return -1

#   retrieves the messages sent to the bot
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    if js != -1:
        return js
    else:
        return -1

#   gets the id of the message that is sent most recently
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#   builds the customized keyboard
def build_keyboard(items, command, indicator, updt_val=""):
    if indicator == 0:
        keyboard = [[command + item[0] + " " + item[1] + " " + updt_val] for item in items]
    else:
        keyboard = [[command + item + " " + updt_val] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

#   sends a message from bot
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)







